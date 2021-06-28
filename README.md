# FAQ

### What is the current calendar week?

see http://www.whatweekisit.org/

### What and when does github compile and send the report?

Every monday morning, at around 9:30, github takes all reports from the last week, compiles them into a pdf and a formatted email and sends both to the secretariat. If your report does not follow the correct naming or is not there, there will be a big fat **missing** instead of your report in the compilation.

### I want to change how often and when the report is compiled and sent.

You can change the respective github actions cron job [take a look here](https://github.com/agricolab/weekly-ppp/blob/main/.github/workflows/send_last_week.yml#L7) You can look up the syntax e.g. at [crontab guru](https://crontab.guru/).

### How do i set up my email client and who receives the report?

Configure the github secrets as described in [githubs documentation](https://docs.github.com/en/actions/reference/encrypted-secrets). You should set the following secrets (mind the spelling):

- SENDER_EMAIL (the mail address used for sending, e.g. `your.account@gmail.com`)
- SMTPHOST (your mail providers host, e.g. `smpt.gmail.com`)
- PASSWORD (the password to the account of the sender)

The other two have sensible defaults, but you better set them, too.
- PORT (your mail providers port, defaults to `587`)
- RECEIVER_EMAIL (the email of the receiver, defaults to the sender email address)

###### Note

Sadly, google mail does not work robustly, and flags the weekly login attempts as fraudulent. You better use a less strict email provider.

### But i want to send weekly reports to multiple subscribers.

The easiest way is to create a [google group](https://support.google.com/a/answer/9400082?hl=en), let everyone who should receive the mail subscribe to the group and forward the email to the group from within your mail account.

### How do i add an report?

Create a subfolder with your name `firstname-lastname` in the folder `personal-reports`. Add a report with the correct filename (`YYYY-CW.md`, e.g. `2021-15.md`) and fill it with markdown formatted text. You can use the file editor included in github for this: https://docs.github.com/en/github/managing-files-in-a-repository/editing-files-in-your-repository

### What do i add in an report?

The report should follow the [PPP scheme](https://en.wikipedia.org/wiki/Progress,_plans,_problems) (Progress, Planned, Problems), which is ideally implemented as paragraphs with respective headings. You should use short bulletpoints only (maybe limit yourself to [72 characters?](https://www.reddit.com/r/git/comments/20ko8g/why_do_a_lot_of_developers_apply_a_72character/)). If you feel a longer format is necessary, put it in your projects repo or in the paper draft, and refer to those in the report. See also the [example](personal-reports/test-candidate/1950-1.md) of the exemplary employee test-candidate.

### How do i create a folder with my name?

You cannot create an empty folder and then add files to that folder, but rather creation of a folder must happen together with adding of at least a single file. This is because git doesn't track empty folders.

On GitHub you can do it this way:

- Go to the folder inside which you want to create another folder
- Click on New file
- On the text field for the file name, first write the folder name you want to create
- Then type /. This creates a folder
- You can add more folders similarly
- Finally, give the new file a name (for example, .gitkeep which is conventionally used to make Git track otherwise empty folders; it is not a Git feature though)
- Finally, click Commit new file.

[Reference](https://stackoverflow.com/questions/12258399/how-do-i-create-a-folder-in-a-github-repository)

### Can i add additonal files which will be ignored?

Generally, any file in your folder ending in `.md` needs to follow the `year-cw.md` regime. Otherwise, the compiler might throw an error, and block also all other reports! Therefore, yes,  you can add any additional files, as long as they do not end with `.md`.  This can be a feature, e.g. adding `gantt-chart.txt` or `year-plan.txt` can be sensible. Yet, it is better if you put those files into the `projects-information` folder, ideally within your own `firstname-lastname` or `project-acronym` subfolder. You should also not push figures on github, because storage space is limited. It is better to publish figures (on https://imgur.com/ or https://figshare.com/ and link to them.

### How do i write markdown?

A nice overview can be found here: https://guides.github.com/features/mastering-markdown/

The key syntax you need to remember are headings, lists, and figures.

Headings are just a line of text, which is prefixed with one ore more `# `, like `#### bullet points` which renders t0

#### bullet points

You can also create unordered lists, i.e. bullet points, which go like

```
- bullet
- point
```

to render like

- bullet
- point

and add figures like

```
![place-kitten](https://placekitten.com/96/140)
```

to render like

![place-kitten](https://placekitten.com/96/140)

If you want to have a preview online, consider that you can `preview changes` in the browser with github (look at the upper left corner of your file editor).

### Can i preview my md or pdf locally?

If you want to have a lcoal preview of your markdown, try https://shd101wyy.github.io/markdown-preview-enhanced/#/ for Atom or VS Code together with pandoc, or simply run pandoc on your local markdown file. Because we compile the `.pdf` from `.md` with pandoc and texlive, you can also use a limited amount of latex commands.

### What happens after i submitted my report?

Github actions automatically compiles all reports of all colleagues to a markdown for each calendarweek. Immediatly after pushing, a yellow dot will appear next to the commit name in the upper right corner. If it turns red, something went wrong, most likely some file has a wrong name. If it turns green, the compilation was successfull.

### Where is the compiled file?

After the action has run sucessfully, click on Actions (right next to Issues and Pull Requests, in the top menu). Click on the upper most commit (that likely has a telling name like `Create 2021-15.md`. You will then find a zip file with this workflows Artifacts, containing the aggregated `.md`.

### But i want a .pdf!

Click on Actions (right next to Issues and Pull Requests, in the top menu).
Select your desired workflow.
Click on run workflow on the right side.
After the workflow has run sucessfully, you will then find a zip file in its Artifacts, containing the aggregated `.md` and a compiled `.pdf`.
