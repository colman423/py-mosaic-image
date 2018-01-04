$(function() {
    $('#file').on('change', function() {
        if (this.files && this.files[0]) {
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
        console.log("submit click!");
        file = $('#base64').text();
        if(!file) {
            alert('no image');
            return;
        }
        let imgData = file.substr(file.indexOf('base64,')+7);
        $.ajax({
            type: "POST",
            url: "/",
            data: { 'file': imgData, 'grid': 10 },
            success: function(res) {
                $('#result').text("start");
                startSocket();
            },
            error: function(XMLHttpRequest, textStatus, errorThrown) {
                console.log("submit click err");
                console.log("Status: " + textStatus);
                console.log("Error: " + errorThrown);
            }
        });
    });
    function startSocket() {
        let timer = setInterval(function() {
            $.ajax({
                type: "POST",
                url: "/",
                data: { 'wait': true },
                success: function(res) {
                    res = JSON.parse(res.replace(/'/g, "\""));
                    console.log(res);
                    if( res['state']==4 ) {
                        let url = '/output/'+res['content'];
                        $('#output').attr('src', url).prop('hidden', false);
                        clearInterval(timer);
                    }

                },
                error: function(XMLHttpRequest, textStatus, errorThrown) {
                    console.log("Status: " + textStatus);
                    console.log("Error: " + errorThrown);
                }
            });
        }, 1000);
    }
});
