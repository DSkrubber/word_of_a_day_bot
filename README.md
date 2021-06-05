<h1>word_of_a_day_bot</h1>
<h2>simple Telegram bot which sends you english word of a day with it's definition</h2>
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
            <li>Each function parses text.data from prepared url links of 'word of a day' and 'english-russian translator' websites.</li>
            <li>Then drops useless data from html and prepare text information for exporting in word_bot for Telegram bot uses.</li>
        </ul>
    </li>
    <li>Wod_bot: module with bot logic.
        <ul>
            <li>First, a few handler functions are defined. </li>
            <li>Then, those functions are passed to the Dispatcher and registered at their respective places.</li>
            <li>After that the bot is started and runs until we press Ctrl-C on the command line.</li>
        </ul>
    </li>

<i>Note: Press Ctrl-C on the command line or send a signal to the process to stop the
bot.</i>

