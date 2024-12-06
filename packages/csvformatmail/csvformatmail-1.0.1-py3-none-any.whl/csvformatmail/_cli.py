# Copyright 2019-2021, Jean-Benoist Leger <jb@leger.tf>
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import argparse
import textwrap
import sys

import csvspoon
import argcomplete
import jinja2

from csvformatmail.mail import Mailer, Mail


def parseargs():
    parser = argparse.ArgumentParser(
        description=textwrap.dedent(
            """
            A tool to format mails from csv and to send them.

            Mails are formatted as f-string with namespace from csv.
            """
        ),
        epilog=textwrap.dedent(
            """
            Examples:

              - Basic one:
                - A template file can be:
                  > From: Me <my-mail-address@example.org>
                  > To: {{email}}
                  > Bcc: my-mail-address@example.org
                  > Subject: Your results
                  >
                  > Hi {{name.capitalize()}},
                  >
                  > You obtain the following result {{result}}, with the value {{"{:.1f}".format(value)}}.
                  >
                  > -- 
                  > me

                - With a csv file containg columns email, name, result, value.

                - With the command:
                    %(prog)s template.txt -t value:float listing.csv

              - More complex template file:
                  > From: Me <my-mail-address@example.org>
                  > To: {{email}}
                  > Bcc: my-mail-address@example.org
                  > Subject: Your results
                  >
                  > Hi {{name.capitalize()}},
                  >
                  > You obtain the following result {{result}}, with the value {{"{:.1f}".format(value)}}.
                  > For information, for results for the class are:
                  >  - mean: {{np.mean(allrows['value'])}}
                  >  - standard deviation: {{np.std(allrows['value'])}}
                  >
                  > -- 
                  > me
                With the command:
                    %(prog)s template.txt --np -t value:float listing.csv
            """
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        add_help=False,
    )
    parser.add_argument(
        "--version", action="version", version="", help=argparse.SUPPRESS
    )
    parser.add_argument(
        "--help",
        action="help",
        default=argparse.SUPPRESS,
        help=argparse._("show this help message and exit"),
    )
    parser.add_argument(
        "-d",
        "--delim",
        dest="delim",
        default=",",
        help="Input delimiter. (default: ',')",
    )
    parser.add_argument(
        "-b",
        "--before",
        action="append",
        default=[],
        help="""
            Run the following code before evaluate the expression on each row.
            Can be specified multiple times. (e.g. "import math").
            """,
    )
    parser.add_argument(
        "--np",
        "--numpy",
        action="store_true",
        help="""
            Quick alias to `--before "import numpy as np"`
            """,
    )
    parser.add_argument(
        "-t",
        "--type",
        action="append",
        type=csvspoon.ColType,
        default=[],
        help="""
            Apply type conversion on specified command prior to expression. The
            argument must be a column name followed by a valid Python type. See
            "--before" to define non standard type. e.g. "a_column:int" or
            "a_column:float". This option can be specified multiple time to type
            different columns.
            """,
    )
    parser.add_argument(
        "-h",
        "--host",
        default="localhost",
        help="""
            SMTP host (default: localhost)
            """,
    )
    parser.add_argument(
        "-p",
        "--port",
        default=0,
        type=int,
        help="""
            SMTP port (default: 587 if STARTTLS enabled else 25)
            """,
    )
    parser.add_argument(
        "--starttls",
        default=False,
        action="store_true",
        help="""
            Enable TLS with STARTTLS.
            """,
    )
    parser.add_argument(
        "-l",
        "--login",
        default=None,
        type=str,
        help="""
            Login used for authentification on SMTP server. Implies STARTTLS."
            """,
    )
    parser.add_argument(
        "--allrows-name",
        default="allrows",
        help="""
            Dict used to access for each column the value of all rows. See
            example. Must not be a valid column name. (default: 'allrows').
            """,
    )

    parser.add_argument(
        "--without-confirm",
        action="store_true",
        help="""
            Send mails without confirmation.
            """,
    )

    parser.add_argument(
        "--wait",
        "-w",
        default=0.0,
        type=float,
        help="""
            Wait time between mail, In seconds. (default: 0s)
            """,
    )

    parser.add_argument(
        "template",
        help="""
            Template file. Must contains header, a empty line, and mail content.
            Header must contains lines From, To and Subject. Other header (as
            Bcc) can be provided.
            Templates are jinja2 template. Each mail is a rendering of the 
            template for each row of the csv file. The template can contain 
            {{val}} to access value of csv file, or more complex construction allowed 
            by jinja2.
            """,
        type=argparse.FileType("r"),
    )

    parser.add_argument(
        "inputcsv",
        help="""
            Input csv file. Must contains columns which are used in template.
            Typing can be applied, see '-t'. Delimiter can be changed, see '-d'.
            """,
        type=csvspoon.CsvFileSpec,
    )

    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    return args


def main():
    args = parseargs()
    template_raw = args.template.read()
    try:
        template = jinja2.Template(template_raw, undefined=jinja2.StrictUndefined)
    except Exception as exc:
        print(
            f"Error when building the template: {exc.__class__}\n{exc}", file=sys.stderr
        )
        sys.exit(1)
    input_csv = csvspoon.ContentCsv(filespec=args.inputcsv, delim=args.delim)
    fake_global = {"__name__": "__main__"}
    before_np = ["import numpy as np"] if args.np else []
    for before in before_np + args.before:
        ast = compile(before, "<string>", "exec")
        exec(ast, fake_global)

    for t in args.type:
        t.build_type(fake_global)
        input_csv.add_type(*t.get_coltype)
    starttls = args.starttls
    password = None
    if args.login is not None:
        login = args.login
        starttls = True
    else:
        login = None
    port = args.port
    if port == 0:
        port = 587 if starttls else 25
    mailer = Mailer(args.host, port, starttls=starttls, login=login, password=password)
    rows = list(input_csv.rows_typed)
    cols = {c: [r[c] for r in rows] for c in input_csv.fieldnames}
    for row in rows:
        if args.allrows_name not in input_csv.fieldnames:
            row[args.allrows_name] = cols
        try:
            mail = Mail(template, row, fake_global)
        except Exception as exc:
            print(
                f"Error when rendering mail: {exc.__class__}\n{exc}",
                file=sys.stderr,
            )
            sys.exit(1)
        mailer.add_mail(mail)
    if args.without_confirm:
        mailer.send_mails(args.wait)
    else:
        mailer.prompt(args.wait)


if __name__ == "__main__":
    main()
