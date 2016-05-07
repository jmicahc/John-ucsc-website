
/**
 * jspsych-survey-likert
 * a jspsych plugin for measuring items on a likert scale
 *
 * Josh de Leeuw 
 *
 * Highly adapted by John Collins.
 * 
 * documentation: https://github.com/jodeleeuw/jsPsych/wiki/jspsych-survey-likert
 *
 */

(function($) {
    jsPsych['survey-likert'] = (function() {

        var plugin = {};

        plugin.create = function(params) {
            
            params = jsPsych.pluginAPI.enforceArray(params, ['data']);
            
            var trials = [];
            for (var i = 0; i < params.stimuli.length; i++) {
                    trials.push({
                        type: "survey-likert",
                        stimuli: params.stimuli[i],
                        is_html: params.is_html,
                        questions: params.questions,
                        labels: params.labels,
                        intervals: params.intervals,
                        show_ticks: (typeof params.show_ticks === 'undefined') ? true : params.show_ticks,
                        data: (typeof params.data === 'undefined') ? {} : params.data[i]
                    });
            }
            return trials;
        };

        plugin.trial = function(display_element, block, trial, part) {
            // if any trial variables are functions
            // this evaluates the function and replaces
            // it with the output of the function
            trial = jsPsych.pluginAPI.normalizeTrialVariables(trial);

            if (!trial.is_html) {
                display_element.append($('<img>', {
                    "src": trial.stimuli,
                    "id": 'survey-likert'
                }));
                $('#survey-likert').css({"margin-left": "185px"});
            }
            else {
                display_element.append(trial.stimuli);
            }

            

            // add likert scale questions
            var i;
            for (i = 0; i < trial.questions.length; i++) {
                console.log(trial.questions);
                // create div
                display_element.append($('<div>', {
                    "id": 'jspsych-survey-likert-' + i,
                    "class": 'jspsych-survey-likert-question',
                    "style": "opacity: 0"
                }));
                
 
                // add question text
                $("#jspsych-survey-likert-" + i).append('<p class="jspsych-survey-likert-text survey-likert">' + trial.questions[i] + '</p>');

                // create slider.
                $("#jspsych-survey-likert-" + i).append($('<div>', {
                    "id": 'jspsych-survey-likert-slider-' + i,
                    "class": "jspsych-survey-likert-slider jspsych-survey-likert"
                }));

                console.log(Math.ceil(trial.intervals[i] / 2));
                $("#jspsych-survey-likert-slider-" + i).slider({
                    value: Math.ceil(trial.intervals[i] / 2),
                    min: 1,
                    max: trial.intervals[i],
                    step: 1,
                    change: function(event, ui) {
                      var c = "#" + this.id + " > a";
                      console.log(c);
                      console.log(this.id);
                      $(c).show(); }
                });
                $('a.ui-slider-handle').hide();

                // show tick marks
                if (trial.show_ticks) {
                    $("#jspsych-survey-likert-" + i).append($('<div>', {
                        "id": 'jspsych-survey-likert-sliderticks' + i,
                        "class": 'jspsych-survey-likert-sliderticks jspsych-survey-likert',
                        "css": {
                            "position": 'relative'
                        }
                    }));
                    for (var j = 1; j < trial.intervals[i] - 1; j++) {
                        $('#jspsych-survey-likert-slider-' + i).append('<div class="jspsych-survey-likert-slidertickmark"></div>');
                    }

                    $('#jspsych-survey-likert-slider-' + i + ' .jspsych-survey-likert-slidertickmark').each(function(index) {
                        var left = (index + 1) * (100 / (trial.intervals[i] - 1));
                        $(this).css({
                            'position': 'absolute',
                            'left': left + '%',
                            'width': '1px',
                            'height': '100%',
                            'background-color': '#222222'
                        });
                    });
                }

                // create labels for slider
                $("#jspsych-survey-likert-" + i).append($('<ul>', {
                    "id": "jspsych-survey-likert-sliderlabels-" + i,
                    "class": 'jspsych-survey-likert-sliderlabels survey-likert',
                    "css": {
                        "width": "100%",
                        "margin": "10px 0px 0px 0px",
                        "padding": "0px",
                        "display": "block",
                        "position": "relative"
                    }
                }));
                console.log('test 10');

                for (var j = 0; j < trial.labels[i].length; j++) {
                    $("#jspsych-survey-likert-sliderlabels-" + i).append('<li>' + trial.labels[i][j] + '</li>');
                }
                display_element.append('<br><br>');

                // position labels to match slider intervals
                var slider_width = $("#jspsych-survey-likert-slider-" + i).width();
                var num_items = trial.labels[i].length;
                var item_width = slider_width / num_items;
                var spacing_interval = slider_width / (num_items - 1);

                $("#jspsych-survey-likert-sliderlabels-" + i + " li").each(function(index) {
                    $(this).css({
                        'display': 'inline-block',
                        'width': item_width + 'px',
                        'margin': '0px',
                        'padding': '0px',
                        'text-align': 'center',
                        'position': 'absolute',
                        'left': (spacing_interval * index) - (item_width / 2)
                    });
                });
                console.log('test 20');
            }

            // add submit button
            display_element.append($('<button>', {
                'id': 'jspsych-survey-likert-next',
                "class": 'jspsych-survey-likert-question',
                "style": 'opacity:0;'
            }));

            var startTime;
            $('video').bind("ended", function() {
               startTime = (new Date()).getTime();
               $('.jspsych-survey-likert-question').css({"opacity": "1"});
            });


            $("#jspsych-survey-likert-next").html('Submit');
            console.log('hello world'); 
            $("#jspsych-survey-likert-next").click(function() {
                // do nothing if no selection taken.
                if( !$('a.ui-slider-handle').is(":visible") ) {
                    return;
                };

                // measure response time
                var endTime = (new Date()).getTime();
                var response_time = endTime - startTime;

                // create object to hold responses
                var question_data = {};
                console.log('test 1');
                console.log($("div.jspsych-survey-likert-slider"));
                $("div.jspsych-survey-likert-slider").each(function(index) {
                    console.log('extending data object');
                    var id = "Q" + index;
                    var val = $(this).slider("value");
                    var obje = {};
                    obje[id] = val;
                    $.extend(question_data, obje);
                });
                console.log('test 2');

                // save data
                block.writeData($.extend({}, {
                    "trial_type": "survey-likert",
                    "trial_index": block.trial_idx,
                    "rt": response_time
                }, question_data, trial.data));

                display_element.html('');

                // next trial
                block.next();
            });
        };

        return plugin;
    })();
})(jQuery);
