$(function() {
    $('#prev').on('click', function() {
        $('#file').click();
    })
    $('#file').on('change', function() {
        if (this.files && this.files[0]) {
            $('#show').hide();
            $('#select').show();
            var FR = new FileReader();
            FR.addEventListener("load", function(e) {
                let code = e.target.result;
                $('#prev').attr('src', code);
                $('#base64').text(code);
            });
            FR.readAsDataURL( this.files[0] );
        }
    });
    $('#submit').on('click', function() {
        file = $('#base64').text();
        if(!file) {
            $('#no-img-err').show();
        }
        else {
            $('#select').hide();
            $('#show').show();
            $('#file').prop('disabled', true);
            $('#no-img-err').hide();

            let imgData = file.substr(file.indexOf('base64,')+7);
            let grid = $('#grid').val();
            $.ajax({
                type: "POST",
                url: "/",
                data: { 'file': imgData, 'grid': grid ? grid : 10},
                success: function(res) {
                    responseProgress(res);
                },
                error: function(XMLHttpRequest, textStatus, errorThrown) {
                    console.log("submit click err");
                    console.log("Status: " + textStatus);
                    console.log("Error: " + errorThrown);
                }
            });
        }
    });
    function responseProgress(uid) {
        console.log("my uid = "+uid);
        $.ajax({
            type: "POST",
            url: "/",
            data: { 'uid': uid },
            success: function(res) {
                res = JSON.parse(res.replace(/'/g, "\""));
                console.log(res);
                let state = res['state'];
                let content = res['content']
                if( res['state']==4 ) {
                    let url = '/output/'+content;
                    $('#output').attr('src', url).prop('hidden', false);

                    $('#progress-text').text("complete!");
                    $('#progress-bar').progressbar("value", 100);

                    $('html,body').animate({
                        scrollTop: $("#output").offset().top
                    },
                    'slow');

                    $('#file').prop('disabled', false);
                }
                else {
                    let text = "";
                    if( state==0 ) text="loading image";
                    else if( state==1 ) text="cutting image";
                    else if( state==2 ) text="finding tiles";
                    else if( state==3 ) text="assembling new image";
                    else text="Oops! error here QAQ";

                    $('#progress-text').text(text);
                    $('#progress-bar').progressbar("value", content);
                    setTimeout(function() {
                        responseProgress(uid);
                    }, 1000);
                }

            },
            error: function(XMLHttpRequest, textStatus, errorThrown) {
                console.log("Status: " + textStatus);
                console.log("Error: " + errorThrown);
            }
        });
    }

    $('#progress-bar').progressbar({
      "ui-progressbar": "ui-corner-all",
      "ui-progressbar-complete": "ui-corner-right",
      "ui-progressbar-value": "ui-corner-left",
      "create": function(event, ui) {$(this).find('.ui-widget-header').css({'background-color':"#67f9c8eb"})}
    });

});
