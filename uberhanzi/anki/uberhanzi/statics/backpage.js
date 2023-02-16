var data;
var debugField = $('#debug');
window.onerror = function(message, source, lineno, colno, error) {
    debugField.append("<br>Message: "+message+" - Source: "+source+" - LineNo: "+lineno+" - ColNo: "+colno+" - Error: "+error);
};
try {
    data = JSON.parse(b64DecodeUnicode($('#data').html()));
} catch (e) {
    data = {};
    debugField.append("JSON parse error. " + e.message);
}

var fonts = [1]; //, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]; // todo if you want more, check HTML in template -> renderFonts(), also check CSS
var amountOfFontsToShow = 1;
var readings = $('#play-sound').text().trim().split(".");
var hanziField = $('#hanzi');
var freqField = $('#frequency');
var confusions = extractConfusions();
// Top
// $('#meanings').text(data.meanings); // no meanings on top, useless

// Metadata
function renderMetaData() {
    var components = '';
    $.each(data.cmp, function (i, value) {
        components += value+'<br>'
    });

    var table = '<div class="metadata-content"><table>';
    table += '<tr><td>Meanings</td><td>' + data.mng + '</td></tr>';
    table += '<tr><td>Components</td><td>' + components + '</td></tr>';
    table += '<tr><td>Pinyin</td><td>' + data.pyn + '</td></tr>';
    if (data.trd) {
        table += '<tr><td>Traditional Form</td><td>' + data.trd + '</td></tr>';
    }
    table += '<tr><td>Frequency</td><td>' + freqField.text() + '</td></tr>';
    table += '</table></div>';
    $('#rendered-content').html(table);
}

function incrementCount(reading, readingCounts, type) {
    var counts = readingCounts[reading];
    if (counts) {
        readingCounts[reading] = {
            total: ++counts.total,
            fnKJ: type === "fnKJ" ? ++counts.fnKJ : counts.fnKJ,
            fnKN: type === "fnKN" ? ++counts.fnKN : counts.fnKN
        };
    } else {
        readingCounts[reading] = {
            total: 1,
            fnKJ: type === "fnKJ" ? 1 : 0,
            fnKN: type === "fnKN" ? 1 : 0
        };
    }
}

function getRandomFontIds(n) {
    var result = new Array(n),
        len = fonts.length,
        taken = new Array(len);
    if (n > len)
        throw new RangeError("getRandom: more elements taken than available");
    while (n--) {
        var x = Math.floor(Math.random() * len);
        result[n] = fonts[x in taken ? taken[x] : x];
        taken[x] = --len in taken ? taken[len] : len;
    }
    return result;
}

function renderFonts(amount, breakAfter) {
    var kanji = hanziField.text();
    var container = '<div class="fonts">';
    var count = 1;
    $.each(getRandomFontIds(amount), function (i, value) {
        container += '<span class="kanji font-' + value + '">' + kanji + '</span>';
        if (count++ % breakAfter === 0) {
            container += '<br>';
        }
    });

    container += '</div>';
    $('#rendered-content').html(container);
}

function renderFontSelection() {
    var ids = getRandomFontIds(amountOfFontsToShow);
    var hanzi = "";
    if (data.trd) {
        hanzi += data.cur+"<br><span class='kanji-highlight'>"+data.trd+"</span>"
    } else {
        hanzi += "<span>"+data.cur+"</span>"
    }
    var html = '';
    $.each(ids, function (index, value) {
        html += '<div class="kanji font-' + value + '">' + hanzi + '</div>'
    });
    $('#side-fonts').html(html);
}

function renderMdbg() {
    var hanzi = hanziField.text();
    $('#rendered-content').html('<iframe class=\"embed\" src=\"https://www.mdbg.net/chinese/dictionary?page=worddict&wdrst=0&wdqb=*' + hanzi + '*\"></iframe>');
}

function renderMdbgWord(word) {
    $('#rendered-content').html('<iframe class=\"embed\" src=\"https://www.mdbg.net/chinese/dictionary?page=worddict&wdrst=0&wdqb=' + word + '\"></iframe>');
}

function renderWordTable() {
    var words = data.exm;
    var title = "Word Examples";

    // Find longest word (for <td> width)
    var maxLength = 1;
    $.each(words, function (index, word) {
        if (word.cur.length > maxLength) {
            maxLength = word.cur.length;
        }
    });
    var tdWidth = maxLength * 23 + 10;

    var table = "<div><h2 style='text-align: center'>" + title + "</h2><table id='example-table' class='example-table'>";
    table += '<thead><tr><th>Word</th><th>Rdg</th><th>Meanings</th><th>Trd</th></tr></thead><tbody>';
    $.each(words, function (index, word) {
        table += '<tr>';
        table += '<td align="center" class="word" style="width: ' + tdWidth + 'px"><a class="kanji-link" href="#modal" rel="modal:open" onclick="fillModal(\'' + toEncodedJson(word) + '\')"><ruby>' + word.cur + '<rt>' + word.pyn + '</rt></ruby></a></td>';
        table += '<td onclick="filterSearch(\'' + findMatchingPinyin(word.pyn) + '\')" class="reading-column">' + word.pyn + '</td>';
        table += '<td>' + word.mng + '</td>';
        table += getTradColumn(word);
        table += '</tr>';
    });
    table += "</tbody></table></div>";

    $('#rendered-content').html(table);
    $(document).ready(function () {
        $('#example-table').DataTable({
            /* No ordering applied by DataTables during initialisation */
            "order": [],
            "pageLength": 100
        });
    });
}

function findMatchingPinyin(wordAsPinyin) {
    var match = "???"
    $.each(data.pyn, function (index, pinyin) {
        if (wordAsPinyin.includes(pinyin)) {
            match = pinyin;
        }
    });
    return match;
}

function getTradColumn(word) {
    if (word.trd) {
        return '<td class="word word-link small-column" onclick="renderMdbgWord(\'' + word.trd.trim() + '\')">' + word.trd + '</td>';
    }
    return '<td>-</td>'
}

function renderButtonTexts() {
    $('#wordExamples').text('Word Examples');
}

function toEncodedJson(word) {
    var obj = {};
    obj.word = word.cur;
    if (data.isTrd) {
        obj.word = word.trd;
    }
    obj.reading = word.pyn;
    obj.foundKanjiReading = findMatchingPinyin(word.pyn);
    obj.meanings = word.mng;
    return btoa(encodeURIComponent(JSON.stringify(obj)));
}

function fillModal(encodedJson) {
    var term = JSON.parse(decodeURIComponent(atob(encodedJson)));
    var meaningsArray = term.meanings.split("<br>");
    var firstMeaning = meaningsArray[0].replace(/\([^\(]*(noun|verb|adjective|adverb|expression)[^\)]*\)/i, "").trim();
    // firstMeaning = firstMeaning.replace(/,.*$/, "").trim();

    var text = "<ruby>" + term.word + "<rt>" + term.reading + "</rt></ruby> (" + term.foundKanjiReading + ", " + firstMeaning + ")";

    $('#word-area').val(text);
    $('#modal-meanings').html(term.meanings);
    updateRuby();
    copyWord(text);
}

function updateRuby() {
    $('#modal-result').html($('#word-area').val());
}

// Doesn't work in Anki. Probably browser too old.
function copyWord(text) {
    var $temp = $("<input>");
    $("body").append($temp);
    $temp.val(text).select();
    document.execCommand("copy");
    $temp.remove();
}

// No use on mobile, only annoying.
function selectOnClick(element) {
    // element.select();
    // try {
    //     element.setSelectionRange(0, 99999);
    // } catch (err) {
    // }
}

function appendSearchOnClickToRubyElements() {
    $.each($('#manual-edits-mnemonic').find('ruby'), function (index, element) {
        var search = element.innerHTML.replace(/<rt.*/, "").replace(/<\/?span.*?>/g, "");
        $(element).click(function () {
            filterSearch(search);
        });
    });
}

var mnemonicFull = $('#manual-edits-mnemonic').clone();

function showMnemonic() {
    if (isToggled) {
        var words = "";
        $.each($(mnemonicFull).find('ruby'), function (index, value) {
            words += "<ruby>" + value.innerHTML.replace(/<.*>/, "") + "</ruby><br>";
        });
        $('#manual-edits-mnemonic').html(words);
    } else {
        $('#manual-edits-mnemonic').html(mnemonicFull.html());
    }
    highlightKanjiInMnemonic();
    makeCommentsGray();
}

function makeCommentsGray() {
    var element = $('#manual-edits-mnemonic');
    var mnemonic = element.html();
    var commentRegex = new RegExp("# ?<ruby.*?ruby>.*?(<(br>)?|\n)");
    var extract = commentRegex.exec(mnemonic);
    var i = 1;
    var replacements = [];

    while (extract !== null) {
        var marker = "@" + i + "@";
        var cleanExtract = extract[0]
            .replace(/<$/, "")
            .replace(/#/, "<span class='bighash'>#</span>")
            .replace(/class="highlight"/g, "");
        var replacement = "<span class='comment'>" + cleanExtract.replace(/<$/, "") + "</span>";
        replacements.push({marker: marker, replacement: replacement});
        mnemonic = mnemonic.replace(commentRegex, marker);
        extract = commentRegex.exec(mnemonic);
    }
    $.each(replacements, function (index, value) {
        mnemonic = mnemonic.replace(value.marker, value.replacement);
    });
    element.html(mnemonic);
}

var isToggled = false;

function toggleFurigana() {
    showMnemonic();
    addHighlightsToMnemonicField();
    appendSearchOnClickToRubyElements();
    isToggled = !isToggled;
}

function filterSearch(value) {
    $("input[type='search']").val(value).trigger("input");
}


function highlightKanjiInMnemonic() {
    var kanji = hanziField.text();

    // Regex
    var kanjiRegex = new RegExp(String(kanji));
    var rubyRegex = new RegExp("<ruby.*?ruby>\\s\\(.*?,");
    var readingRegex = new RegExp("\\(.*?,");

    var element = $('#manual-edits-mnemonic');
    var mnemonic = element.html();
    var extract = rubyRegex.exec(mnemonic);
    var i = 1;
    var replacements = [];
    while (extract !== null) {
        var marker = "#" + i + "#"; // replace occurrence with marker, for later replacement
        var reading = toHiragana(readingRegex.exec(extract[0])[0].replace(/[^\w]/, "").replace(",", ""));
        var replacement = "";
        if (extract[0].indexOf("?") === -1) {
            replacement = extract[0]
                .replace(kanjiRegex, "<span class='highlight'>" + kanji + "</span>")
                .replace(reading, "<span class='highlight'>" + reading + "</span>");
        } else {
            replacement = extract[0];
        }
        replacements.push({marker: marker, replacement: replacement});

        mnemonic = mnemonic.replace(rubyRegex, marker);
        extract = rubyRegex.exec(mnemonic);
        i++;
    }

    $.each(replacements, function (index, value) {
        mnemonic = mnemonic.replace(value.marker, value.replacement);
    });

    element.html(mnemonic);
}

function highlightUnclassifiedReadings() {
    var hasCommonWords = false;
    $.each(data.unclassifiedReadings, function (index, word) {
        if (word.freqNF <= 20000 || word.freqWK <= 20000) {
            $('#unclassifiedReadings').attr('style', 'background-color: rgba(140, 175, 73, 0.6)');
            return false;
        }
        if (word.score >= 1) {
            hasCommonWords = true;
        }
    });
    if (hasCommonWords) {
        $('#unclassifiedReadings').attr('style', 'background-color: rgba(113, 175, 36, 0.31)');
    }
}

function addHighlightsToMnemonicField() {

    // Ruby highlighting
    var mnemonicField = $('#manual-edits-mnemonic');
    var sections = mnemonicField.html().split(/---+/);
    if (sections[1]) {
        sections[1] = deleteFirstBreak(sections[1]);
        sections[1] = sections[1].trim() !== "" ? "<div class='section-fnkj section-box'>" + sections[1] + "</div>" : "";
    }
    if (sections[2]) {
        sections[2] = deleteFirstBreak(sections[2]);
        sections[2] = sections[2].trim() !== "" ? "<div class='section-fnkn section-box'>" + sections[2] + "</div>" : "";
    }
    if (sections[3]) {
        sections[3] = deleteFirstBreak(sections[3]);
        sections[3] = sections[3].trim() !== "" ? "<div class='section-ofrm section-box'>" + sections[3] + "</div>" : "";
    }
    if (sections[4]) {
        sections[4] = deleteFirstBreak(sections[4]);
        sections[4] = sections[4].trim() !== "" ? "<div class='section-notes section-box'>" + sections[4] + "</div>" : "";
    }

    // !done marker highlight
    var html = sections.join("");
    html = addDoneMarker(html);
    html = addConfMarker(html);
    html = addNewMarker(html);

    mnemonicField.html(html);
}

function addConfMarker(html) {
    if (confusions.length > 0) {
        html += "<div style='margin-top: 5px'><span class='confusion'>Confusions: </span>";
        for (var kanji of confusions) {
            var conf = confMap[kanji.trim().codePointAt(0).toString(16)];
            html += "<br>" + conf.meta;
        }
        html += "<br></div>"
    }

    return html;
}

function extractConfusions() {
    try {
        var kanji = hanziField.text().trim().codePointAt(0).toString(16); // as unicode
        if (confMap[kanji]) {
            return confMap[kanji].confs;
        }
    } catch (e) {
        debugField.append(e);
    }
    return [];
}

function addDoneMarker(html) {
    if (html.indexOf("!done") > -1) {
        html = html.replace(/!done/, "");
        html += "<div class='done'>DONE</div>"
    }
    return html;
}

function addNewMarker(html) {
    // var regex = new RegExp("!new\\s?(\[.*?\])");
    var regex = new RegExp("!new ?.*?\]");
    var extract = regex.exec(html);
    if (extract !== null) {
        var marker = extract[0].replace(/!new ?/, "<div id='new' onclick='searchNew(\"" + extract[0] + "\")'>NEW ") + "</div>";
        html = html.replace(regex, "");
        html += marker;
    }

    return html;
}

function searchNew(value) {
    var term = value.replace(/^!new \[/, "").replace(/]$/, "");
    filterSearch(term);
}

function deleteFirstBreak(segment) {
    return segment.replace(/^\s*<br>/, "");
}

// --------------------------------------------------
// PLAY SOUNDS
// --------------------------------------------------
function playSingleReading(reading) {
    try {
        new Audio(createPathToMp3(reading)).play();
    } catch (err) {
        debugField.append("Couldn't play " + readings[i] + ". Probably file does not exist.");
    }
}

function createPathToMp3(reading) {
    return "uberhanzi/pinyin/" + reading + ".mp3";
}

var sounds = [];
$.each(readings, function (key, val) {
    sounds.push(new Audio(createPathToMp3(val)));
});
var i = -1;

function playCompoundReading() {
    i++;
    if (i === readings.length) {
        i = -1;
        return;
    }
    sounds[i].addEventListener('ended', playCompoundReading);
    sounds[i].play();
    // DOESN'T WORK IN ANKI DROID, JS crashes. TRY-CATCH also doesn't work. Doesn't catch exception, because Audio.play() is a Promise.
    // .catch(function (err) {
    //     $('#debug').html("Couldn't play " + readings[i] + ". Either file does not exist or playback failed.<br>" + err);
    //     i = -1;
    // })
}

// Same as above, but doesn't use Audio in array. Doesn't work
// var i = -1;
// function playCompoundReading() {
//     i++;
//     if (i === readings.length) {
//         i = -1;
//         return;
//     }
//     var audio = new Audio();
//     audio.src = "uberkanji/readings/"+readings[i]+".mp3";
//     audio.addEventListener('ended', playCompoundReading);
//     audio.play();
// }

// Click play button. Doesn't work
// function clickPlay() {
//         $("#click-play").trigger("click");
// }

function playWordReading(kanji, kana) {
    new Audio("https://assets.languagepod101.com/dictionary/japanese/audiomp3.php?kanji=" + kanji.trim() + "&kana=" + kana.trim()).play();
}

// --------------------------------------------------
// KANA CONVERTER
// --------------------------------------------------

var KATAKANA_HIRAGANA_SHIFT = "\u3041".charCodeAt(0) - "\u30a1".charCodeAt(0);

function toHiragana(str) {
    var result = "";
    $.each(str.split(''), function (index, value) {
        if (value > "\u30a0" && value < "\u30f7") {
            result += String.fromCharCode(value.charCodeAt(0) + KATAKANA_HIRAGANA_SHIFT);
        } else {
            result += value;
        }
    });
    return result;
}

function b64DecodeUnicode(str) {
    // Going backwards: from bytestream, to percent-encoding, to original string.
    return decodeURIComponent(atob(str).split('').map(function(c) {
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));
}

// --------------------------------------------------
// EXECUTE ON LOAD
// --------------------------------------------------

playCompoundReading();
renderFontSelection();
renderButtonTexts();
renderMetaData(); // SLOW: renderWordTable('wordExamples');
highlightUnclassifiedReadings();
addHighlightsToMnemonicField();
appendSearchOnClickToRubyElements();
toggleFurigana();
