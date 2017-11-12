var me = {};
me.avatar = "img/CARAstudent.jpg";

var you = {};
you.avatar = "img/CARAVLogothumbnail.png";

function formatAMPM(date) {
    var hours = date.getHours();
    var minutes = date.getMinutes();
    var ampm = hours >= 12 ? 'PM' : 'AM';
    hours = hours % 12;
    hours = hours ? hours : 12; // the hour '0' should be '12'
    minutes = minutes < 10 ? '0'+minutes : minutes;
    var strTime = hours + ':' + minutes + ' ' + ampm;
    return strTime;
}            

//-- No use time. It is a javaScript effect.
function insertChat(who, text, time = 0){
    var control = "";
    var date = formatAMPM(new Date());
    
    if (who == "me"){
        
        control = '<li style="width:100%">' +
                        '<div class="msj macro">' +
                            '<div class="text text-l">' +
                                '<p style="color:black">'+ text +'</p>' +
                                '<p style="color:black"><small>'+date+'</small></p>' +
                            '</div>' +
                    '</li>';                    
    }else{
        control = '<li style="width:100%;">' +
                        '<div class="msj-rta macro">' +
                            // '<div class="text text-r">' +
                            '<p style="color:black">'+ text +'</p>' +
                                '<p style="color:black"><small>'+date+'</small></p>' +
                            // '</div>' +
                        '<div class="avatar" style="padding:0px 0px 0px 10px !important"><img class="img-circle" style="width:10%;" src="'+you.avatar+'" /></div>' +                                
                  '</li>';
    }
    setTimeout(
        function(){                        
            $(".chatbox").append(control);

        }, time);
    
}

function resetChat(){
    $("ul").empty();
}

$(".mytext").on("keyup", function(e){
    if (e.which == 13){
        var text = $(this).val();
        if (text !== ""){
            insertChat("me", text);              
            $(this).val('');
        }
    }
});

//-- Clear Chat
resetChat();



insertChat("cara", "Hi, my name is Cara!", 0);
insertChat("me", "Hi Cara!", 0);
insertChat("me", "Hi Cara!", 0);
insertChat("me", "Hi Cara!", 0);
insertChat("me", "Hi Cara!", 0);
insertChat("me", "Hi Cara!", 0);


//-- NOTE: No use time on insertChat.