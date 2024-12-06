# csvformatmail: A tool to format mails from csv and to send them

## Installing

From pypi:

```
pipx install csvformatmail
```

You can also use `pip` if you do not want to install in a contained environnement.

Or developer version:

```
git clone <this repo>
cd csvformatmail
pip3 install -e .
```

## (Optional) Enable completion (for bash or other shells using bash-completion)

```
mkdir -p ~/.local/share/bash-completion/completions
register-python-argcomplete csvformatmail > ~/.local/share/bash-completion/completions/csvformatmail
```

## Example

Write a mail template:

```
From: My name <my-mail-address@example.org>
To: {{mail}}
Bcc: my-mail-address@example.org
Subject: Result of the last test

Dear {{firstname}} {{lastname.capitalize()}},

Your results of the last test are:

 - Part A: {{"{:.1f}".format(a)}}
 - Part B: {{"{:.1f}".format(b)}}

Therefore you {% if (a+b)/2>=10 %}pass{%else%}fail{%endif%} the test.
{% if (a+b)/2<10 %}
Another test session will be organized soon.
{%endif%}
-- 
Your teacher
```

Use a csv file with (at least) the columns `firstname`, `lastname`, `mail`, `a`
and `b`:

```
firstname,lastname,mail,a,b,c
Jacques,MARTIN,jacques.martin@example.org,12.54441,14,1111.221
…
```

And the command if you use a distant smtp:

```
csvformatmail -h smtp.example.org -l mylogin template.txt -t a:float -t b:float listing.csv
```

Or if you have a local smtp:

```
csvformatmail template.txt -t a:float -t b:float listing.csv
```

## Complex example

The template file can contain python definition, and all the rows for each
column is accessible by the names `allrows` (default name, can be changed with
arg `--allrows-name`). See the following template file:

```
From: My name <my-mail-address@example.org>
To: {{mail}}
Bcc: my-mail-address@example.org
Subject: Result of the last test

Dear {{firstname}} {{lastname.capitalize()}},

Your results of the last test are:

 - Part A: {{"{:.1f}".format(a)}}
 - Part B: {{"{:.1f}".format(b)}}

For you information, the statistics for part A are:
 - mean: {{'{:.2f}'.format(np.mean(allrows['a']))}}
 - standard deviation: {{'{:.2f}'.format(np.std(allrows['a']))}}.

Therefore you {% if (a+b)/2>=10 %}pass{%else%}fail{%endif%} the test.
{% if (a+b)/2<10 %}
Another test session will be organized soon.
{%endif%}
-- 
Your teacher.
```

And the command if you use a distant smtp:

```
csvformatmail -h smtp.example.org -l mylogin template.txt --np -t a:float -t b:float listing.csv
```

## Misc

Consider use function `fill` and `indent` of `textwrap` module. For this you
need use `-b "import textwrap"` or add a python preamble in you template file.
_e.g._ in a template to rewrap to 72 chars:

```
{{textwrap.fill(somevalue, width=72)}}
```

Or, for rewrap and indent by `> `:

```
{{textwrap.indent(textwrap.fill(somevalue, width=70), "> ")}}
```
