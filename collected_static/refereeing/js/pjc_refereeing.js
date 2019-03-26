$(document).ready(function() {
    var $sw_start = $("#sw_start");
    var $sw_stop = $("#sw_stop");
    var $sw_time = $("#sw_time");
    var countdown = 150;
    var countdown_running = false;

    $("#btn_config").click(function () {
        $.ajax({
            url: url_rnd_config,
            success: function(data) {
                console.log("config=" + data);
                $("#config").html(data);
                $("#div_config").removeClass("hidden");
                $("#btn_config").addClass("hidden");
            }
        });
    });

    $("a[type='submit']").click(function () {
        $("#result_form").submit();
    });

    $("input[type='number']").TouchSpin({
       min: 0
    });

    $sw_start.click(function () {
        countdown_running = true;
        update_countdown();
        $sw_start.toggleClass("disabled");
        $sw_stop.toggleClass("disabled");
    });

    $sw_stop.click(function () {
        countdown_running = false;
        $sw_start.toggleClass("disabled");
        $sw_stop.toggleClass("disabled");

        if ($used_time_field !== null) {
            var elapsed = 149 - countdown;
            var mins = Math.floor(elapsed / 60);
            var secs = Math.floor(elapsed % 60);
            if (secs < 10) {
                secs = "0" + secs;
            }
            $used_time_field.val("0" + mins + ":" + secs);
        }
    });

    function update_countdown() {
        if (countdown_running) {
            var mins = Math.floor(countdown / 60);
            var secs = Math.floor(countdown % 60);
            if (secs < 10) {
                secs = "0" + secs;
            }
            $sw_time.text(mins + ":" + secs);

            if (countdown > 0) {
                if (countdown === 15) {
                    $sw_time.addClass('text-warning');
                }
                countdown--;
                setTimeout(update_countdown, 1000);
            } else {
                countdown_running = false;
                $sw_time.removeClass('text-warning');
                $sw_time.addClass('text-danger');
                $sw_stop.toggleClass("disabled");
            }
        }
    }
});