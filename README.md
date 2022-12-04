# **awesome-instaling**
[![License](https://img.shields.io/github/license/kotekpsotek/awesome-instaling?logoColor=blueviolet)](https://github.com/kotekpsotek/awesome-instaling/blob/master/LICENSE)
[![Release](https://img.shields.io/github/v/release/kotekpsotek/awesome-instaling?logoColor=blue)](https://github.com/kotekpsotek/awesome-instaling/releases)

## **How it works?**
1. If you use bot first time bot ask you about login data to ***instaling.pl*** page (passoword, login) and when bot coudn't get any data required to login (password or login) then bot will be ask you about unsetted login data up to you add login data which isn't known,
2. You can change passed **instaling.pl** login datas in any time by use ***"-cin"*** or ***"--cinstlog"*** arguments in CLI after pass start bot directive (more infos about arguments you can see under **-h**/**--help** arguments),
3. When every login data is known then bot open browswer window and goes to [instaling.pl login page](https://instaling.pl/teacher.php?page=login), after that bot starts login you using for that your account login data saved before in [login file]("/../config/loginData.json),
4. After success login bot goes to ***Session*** by click on ***"Zacznij codzienną sesję"*** **button**,
5. Next bot is in the session and it starts doing session by pass answers for questions. For get translations for word bot at the first goes to the [translations file](translations/translations.json) and search in this file translations for word which must be transaled. When bot coudn't searched translation for word which must be translated in [file with translations](translations/translations.json) then bot will use **Google Translator API** to get this translation,
6. Recived translation will be pass in field for translations in instaling.pl session,
7. After recived translation and pass it in the field for the word translation bot will check if answer is correct. Bot do one of actions placed below after recived specific result for last answer:
    <ul>
     <li><b>When Answer is <u><i>Correct</i></u> (green text)</b> - then if word which has been used in answer for question isn't saved in <b><i>file with translations</i></b> then this word will be saved in this file</li>
     <li><b>When Answer is <u><i>Totally InCorrect</i></u> (red text)</b> - bad answer has been saved in <b><i>file with bad answers</i></b> for don't answer bad, for the same question in the next trials</li>
     <li><b>When Answer is <u><i>Bit InCorrect</i></u> (blue text) or translation for word cound't be getted</b> - then this word to translate with source question, with word usage will be saved in list with words which cound't be translated placed in the <b><i>file with words which coudn't be translated</i></b>. This operation allow user to add by him translation for word manually. When translation for word placed on the <b>cound't translated words list</b> from some <b>reason</b> has been known then this list is reduced by word for which translation is now known. This <b>reason</b> can be: <i>user add translation for word manually</i> or <i>next answer for this question is <b>Totally InCorrect</b></i> so translation for word upon this place is known</li>
    </ul>
7. After providing all answers for session questions, bot goes to the **inslating.pl user panel** again, then bot will display "session ends!!!" communication in CLI and end his action,
8. You can configure words case type from each answer sentence before launch daily session by launch bot with argument: **--adconfshow true** (More about allowed arguments you can see under arguments: **--help** or **-h**) 

### **Video representing how bot works**:
[youtube video](https://www.youtube.com/watch?v=1Cfe7HCYec8)

## **How to launch bot?**
#### **By CLI using python:**
##### **1 Way**:
1. Go to folder with bot source files,
2. Open CLI,
3. Type: py main.py -> this command starts the bot,

##### **2 Way**:
1. Go to folder with bot source files,
2. Open CLI,
3. Type: py main.py --run true -> this command starts the bot,


#### **By Executable file:**
1. Go to folder where is located bot executable file,
2. Open CLI,
3. Luanch executable file from CLI using specific system command for this

## **CLI arguments:**
- You can use these arguments after bot start directive in followed orders: **run bot**, **configure/change configuration bot in more sophisticated way**, **show configuration config**, **change instaling.pl login datas**,
- To see full list of allowed arguments you must use this command: ```py main.py --help/-h``` (choose one: --help or -h),
- Each argument must be used in this form: ```py main.py [argument] true```,
- Each passed argument must have got assigned boolean **true** (raw = without surrounded quotes)

### **Usage example:**

#### **Show actual additional options configuration - facilitate because you can also perform that by look to [file](./config/ad_config.json)**:<br>
``py main.py --adconfshow true``

#### **Change configured prior instaling.pl login datas**:
``py main.py --cinstlog true``<br>
***OR***<br> 
``py main.py -cin true`` 

#### **Display full arguments list**:
``py main.py --help``<br>
***OR***<br>
``py main.py -h``

## **Releases:**
<table style="table-layout: fixed;">
<tr>
    <th>Release</th>
    <th>Description</th>
</tr>
<tr>
    <td><b>1.0.0</b></td>
    <td>First release of bot. Bot is launched from CLI and works in it</td>
</tr>
</table>

## **Requirements:**
1. Python in version 3.0 or heighter when you would like start bot using Python

## **Instalation:**
1. Click on [release](https://github.com/kotekpsotek/awesome-instaling/releases),
2. Choise the newest release and download compressed files or executable file format included compiled bot code to machine code. Executable file format must be compatible with your system (description which executable file format is for which operating system)

## **What you should know:**
1. Bot has got implemented **Google Translator API** so you should know is that in the moment when you start using it from your computer will be performed communication with Google servers,
2. When you use bot, base of words translations will be multipling so results of sessions will be better each subsequenty use. When you would like to get the best results from the moment when you use bot first time you should manually fill translations for the words about which you know that, them are in the session, to do this you must go to the [translations file](translations/translations.json),
3. Bot is only facilitation for solve daily sessions. Remember that learning is extreamely important and you shoudn't neglect it by using this bot!!!
4. All correct transaltions of words will be saved in [.json translations file](translations/translations.json). Go to this file in free time to teach yourself overdue words!!!

## **Auxiliary materials:**
[video representing how bot works](https://www.youtube.com/watch?v=1Cfe7HCYec8)

## **Getting help:**
If you have got any question, problem or you found bug I encourage you to send message for help [issue](https://github.com/kotekpsotek/awesome-instaling/issues) (click on for ask about help)

## **License:**
Project is distrybuted under the terms of MIT license
