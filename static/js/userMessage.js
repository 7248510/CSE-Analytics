var socket = io.connect("http://" + document.domain);
$(function () {

    // var username = document.getElementById('id');
    var x = 100;
//     document.getElementById('userNameInput').onchange = function() {
//       // let username = document.getElementById('userNameInput').innerHTML;
//       // document.getElementById('userName').display = 'none';
//       this.form.preventDefault();
//       this.form.submit();
// };
// console.log(userName);
    // $('#userName').submit(function(l){
    //   l.preventDefault();
    //   username = $('#userNameInput').val();
    //   console.log(username);
    //   $('#userName').css('visibility', 'hidden');
    //   socket.emit( 'my event', {
    //     user_name : username,
    //     message : 'has connected'
    //   } );
    //   return false;
    // })


    $('#myForm').submit(function(e){
        msg = ($('#bottomBar').val());
        socket.emit( 'my event', {
          user_name : username,
          senderID: userID,
          recieverID: document.getElementById('receiverName').getAttribute("name"),
          message : msg
        } )
          // console.log(username);
      e.preventDefault(); // prevents page reloading
      // socket.emit('chat message', $('#bottomBar').val());
      return false;
    });
    socket.on( 'my response', function( msg ) {
      $('#messages').append('<li><b>' + msg.user_name + '</b>    ' + msg.message + '</li>');
      $('#bottomBar').val('');
      document.getElementById('messages').scrollTop = x;
      x+= 100;
    });
    // socket.on('chat message', function(msg){
    //   $('#messages').append($('<li>').text(msg));
    // });
  });
