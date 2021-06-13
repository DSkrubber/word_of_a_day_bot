<h1>word_of_a_day_bot</h1>
<h3>Simple Telegram bot which sends you english 'word of a day' with it's definition</h3>
<ul>
    <li>Possibilities:
        <ol type="1">
            <li>Send word of a day.</li>
            <li>Set daily timer for sending word of a day in chat.</li>
            <li>Translate words from english to russian and vice versa.</li>
        </ol>
    </li>
    <li>Wod_parser: module with parsing functions using 'requests' lib.
        <ul>
            <li>There are presented different parsing functions to work with wod_bot.py</li>
            <li>Each function parses text.data from prepared url links of 'word of a day' and 
                'english-russian translator' websites.</li>
            <li>Then drops useless data from html and prepare text information for exporting in word_bot 
                for Telegram bot uses.</li>
        </ul>
    </li>
    <li>Wod_bot: module with bot logic.
        <ul>
            <li>First, a few handler functions are defined. </li>
            <li>Then, those functions are passed to the Dispatcher and registered at their respective places.</li>
            <li>After that the bot is started and runs until we press Ctrl-C on the command line.</li>
            <li><strong>Make sure to replace TOKEN in 'main()' function row: 'updater = Updater(TOKEN)' with 'token' 
                    provided by BotFather</strong>
            </li>
        </ul>
    </li>
</ul>
<i>Note: Press Ctrl-C on the command line or send a signal to the process to stop the
bot.</i>
<hr>
<strong> To learn how to add Bot via BotFather in Telegram (visit 
<a href="https://core.telegram.org/bots">https://core.telegram.org/bots</a> to learn how to create bot 
   with Telegram's BotFather
</strong>
<h3>If you want to deploy it via docker:</h3>
<hr>
<ul>
    <li>
        Make sure that Docker process is running and use command:
        <br><code>docker pull skrubber/wod_bot_image:latest</code>
    </li>
    <li>
        After downloading of image use following template of run command:
        <br><br><i><u>Note:</u> 
        <br>Text in square brackets such as "[bracket text]" could be replaced with your values or ignored.
        <br>Text in round brackets such as "{TOKEN or PORT} must be presented and replased by your values!"</i>
        <br><br>
        <code>
            docker run -d [--name wod_bot] -p {8080}:80 -e TO_BOTFATHER={"some_token:123133515"} 
            skrubber/wod_bot_image:latest
        </code>
        <br><br><i><u>Note:</u> 
        <br>If container stops immediatly add <code>tail -f /dev/null</code> in the end of docker run command.</i><br>
        <br>
    </li>
    <li>
        Add Bot via BotFather in Telegram (visit <a href="https://core.telegram.org/bots">
            https://core.telegram.org/bots</a> to learn how to create bot with Telegram's BotFather
    </li>
</ul>
<strong>Feel free to inspect Dockerfile to alter image if needed</strong>
