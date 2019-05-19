$(document).ready(function() {
    // stop watch
    var $btn_sw_start = $("#sw_start");
    var $btn_sw_stop = $("#sw_stop");
    var $sw_time = $("#sw_time");

    var MATCH_DURATION = 150;   // 2mn30
    var match_countdown = MATCH_DURATION;
    var match_countdown_running = false;

    // wall clock
    var $btn_wc_start = $("#wc_start");
    var $wc_time = $("#wc_time");

    var wc_countdown_running = false;
    var wc_countdown = 10 * 60;     // 10mn
    var wc_staging_limit = 7 * 60;
    var wc_staging_warning = 7 * 60 + 30;
    var wc_retry_limit = 4 * 60;

    var staging = true;

    var $btn_submit = $("#btn_submit");
    var $btn_reset = $("#btn_reset");
    var $btn_cancel = $("#btn_cancel");

    var $team_select = $("#id_team");
    var $div_team_dependant = $("#team_dependant");
    var $div_config = $("#div_config");
    var $btn_config = $("#btn_config");

    function reset_input_fields() {
        for (var fld in input_fields) {
            var $fld = $("#id_" + fld);
            if ($fld.is(':checkbox')) {
                if (input_fields[fld]) {
                    $fld.setAttribute("checked", "1");
                } else {
                    $fld.removeAttr("checked");
                }
            } else if ($fld.is(':radio')) {
                alert("Radio controls not supported");
            } else {
                $fld.val(input_fields[fld]);
            }
        }
    }

    // $div_team_dependant.hide();
    $team_select.change(function () {
        if ($team_select.val()) {
            $div_team_dependant.fadeIn();
        } else {
            $div_team_dependant.fadeOut();
        }
    });

    $btn_config.click(function () {
        $.ajax({
            url: url_rnd_config,
            success: function(data) {
                console.log("config=" + data);
                if (! $div_config.hasClass("hidden")) {
                    $div_config.fadeOut("fast", function () {
                        $("#config").html(data);
                    });
                } else {
                    $("#config").html(data);
                    $div_config.removeClass("hidden")
                }

                $div_config.fadeIn("fast");
                if ($btn_config.hasClass("config_only_once")) {
                    $("#btn_config").addClass("hidden");
                }
            }
        });
    });

    $btn_submit.click(function () {
        $("#result_form").submit();
    });

    $("input[type='number']").each(function () {
        $(this).TouchSpin({
            min: $(this).attr("min"),
            max: $(this).attr("max")
        });
    });

    $btn_sw_start.click(function () {
        staging = false;
        match_countdown_running = true;
        update_match_countdown();
        $btn_sw_start.toggleClass("disabled");
        $btn_sw_stop.toggleClass("disabled");

        // starts wall clock if not yet done
        if (!wc_countdown_running) {
            $btn_wc_start.click();
        }

        // disable action buttons to avoid unwanted actions
        $btn_submit.addClass("disabled");
        $btn_reset.addClass("disabled");
        $btn_cancel.addClass("disabled");
    });

    $btn_sw_stop.click(function () {
        match_countdown_running = false;
        $btn_sw_start.toggleClass("disabled");
        $btn_sw_stop.toggleClass("disabled");

        if ($used_time_field !== null) {
            var elapsed = 149 - match_countdown;
            var mins = Math.floor(elapsed / 60);
            var secs = Math.floor(elapsed % 60);
            if (secs < 10) {
                secs = "0" + secs;
            }
            $used_time_field.val("0" + mins + ":" + secs);
        }

        // re-enable action buttons
        // make action buttons active again
        $btn_submit.removeClass("disabled");
        $btn_reset.removeClass("disabled");
        $btn_cancel.removeClass("disabled");
    });

    function update_match_countdown() {
        if (match_countdown_running) {
            var mins = Math.floor(match_countdown / 60);
            var secs = Math.floor(match_countdown % 60);
            if (secs < 10) {
                secs = "0" + secs;
            }
            $sw_time.text(mins + ":" + secs);

            if (match_countdown > 0) {
                if (match_countdown === 15) {
                    $sw_time.addClass('text-warning');
                }
                match_countdown--;
                setTimeout(update_match_countdown, 1000);

            } else {
                match_countdown_running = false;
                $sw_time.removeClass('text-warning');
                $sw_time.addClass('text-danger');
                $btn_sw_stop.toggleClass("disabled");
            }
        }
    }

    $btn_wc_start.click(function () {
        update_wall_clock();
        $btn_wc_start.toggleClass("disabled");
        wc_countdown_running = true;
    });

    function update_wall_clock() {
        var mins = Math.floor(wc_countdown / 60);
        var secs = Math.floor(wc_countdown % 60);
        if (secs < 10) {
            secs = "0" + secs;
        }
        $wc_time.text(mins + ":" + secs);
        // update wall clock display attributes to reflect that
        // a match has been started
        if (match_countdown_running) {
            $wc_time.addClass('text-success');
        }

        if (wc_countdown > 0) {
            switch (wc_countdown) {
                case wc_staging_warning:
                    if (staging) {
                        $wc_time.addClass('text-info');
                    }
                    break;
                case wc_staging_limit:
                    if (staging && !match_countdown_running) {
                        $wc_time.removeClass('text-info');
                        $wc_time.addClass('text-warning');
                    }
                    break;
                case wc_retry_limit:
                    $wc_time.removeClass('text-success');
                    $wc_time.addClass('text-warning');

                    $btn_reset.addClass('disabled');
                    break;
            }

            wc_countdown--;
            setTimeout(update_wall_clock, 1000);

        } else {
            $wc_time.removeClass('text-warning');
            $wc_time.addClass('text-danger');
        }
    }

    $btn_reset.click(function () {
        match_countdown_running = false;
        match_countdown = MATCH_DURATION;

        $sw_time.text("2:30");
        $sw_time.removeClass('text-warning');
        $sw_time.removeClass('text-danger');

        $btn_sw_start.removeClass("disabled");
        $btn_sw_stop.addClass("disabled");

        reset_input_fields();
    });

    if ($("#error-alert").length === 0) {
        $btn_submit.addClass("disabled");
    }
});