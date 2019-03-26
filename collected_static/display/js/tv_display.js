$(document).ready(function() {
    var display_container = $("#display-content");
    var clock_container = $("#clock");
    var error_container = $("#error-message");
    error_container.hide();

    /*
        This function is invoked periodically by auto-rescheduling itself using a timer (see
        end of body).

        It gets the content to be displayed by sending an Ajax request to the server, which replies
        with the HTML code to be put in the content container. Additional data are packaged with the
        returned structure for managing the display sequencing (see success callback of the Ajax call
        for details).
     */
    function update_display() {
        var display_delay = 5; // seconds
        var use_animations = true;

        var url = document.location.href;
        if (url.substr(-1, 1) !== '/') { url += '/'; }
        url += 'content';
        $.ajax({
            url: url,
            dataType: "json",
            timeout: 5000,
            success: function(data) {
                // received data is a dictionary with the following entries:
                // - content (string) : the HTML code to be displayed in the content division
                // - delay (int) : the delay (in seconds) before requesting next display
                // - clock (string) : the server clock at display time
                // - use_animations (bool) : true if animations used for transitions
                display_delay = data.delay;
                use_animations = data.use_animations;
                clock_container.html(data.clock);
                if (use_animations) {
                    display_container.fadeOut('fast', function () {
                        display_container.html(data.content);
                        display_container.fadeIn('fast');
                    });
                } else {
                    display_container.html(data.content);
                }
                error_container.hide();
            },
            error: function(jqXHR, textStatus, errorThrown) {
                if (textStatus === "error") {
                    error_container.show();
                }
            },
            complete: function(jqXHR, textStatus) {
                // reschedule ourselves at the end of the display delay
                setTimeout(update_display, display_delay * 1000);
            }
        });
    }

    // bootstraps the first display
    update_display();
});