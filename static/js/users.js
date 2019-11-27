const urlParams = new URLSearchParams(window.location.search);
const ip = urlParams.get('ip');
function init() {
  if( /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ) {
    window.location.href="mobileUsers?ip=" + ip;
  }
    // Clear forms here
    document.getElementById("file").value = "";
    document.getElementById('uploader').action = "/uploader?ip=" + ip;
    // val = document.getElementById('ipadd').innerHTML + ip;
    // document.getElementById("ipadd").innerHTML = val;
};
function users() {
    window.location.href="/users?ip=" + ip;
}

    var socket = io.connect("http://" + document.domain);
window.onload = init;
console.log(ip);
function stream(){
  window.location.href = "http://" + ip + "/streaming";
}
function firstFunction(_callback){
    // do some asynchronous work
    // and when the asynchronous stuff is complete
    _callback();
}
function showFile(){
  filename = document.getElementById('file').files.item(0).name;
  document.getElementById('filespan').innerHTML = filename;
}
function secondFunction(){
    // call first function and pass in a callback function which
    // first function runs when it has completed
    firstFunction(function() {
        console.log('huzzah, I\'m done!');
    });
}
function results(){
  var url = "/scanResults?ip=" + ip;
  window.location.href=url;
}
function admin(){
  window.location.href = "/userSelect";
}
$(function () {

    var username;
    var x = 100;
//     document.getElementById('userNameInput').onchange = function() {
//       // let username = document.getElementById('userNameInput').innerHTML;
//       // document.getElementById('userName').display = 'none';
//       this.form.preventDefault();
//       this.form.submit();
// };
// console.log(userName);
    $('#userName').submit(function(l){
      l.preventDefault();
      username = $('#userNameInput').val();
      console.log(username);
      $('#userName').css('visibility', 'hidden');
      socket.emit( 'my event', {
        user_name : username,
        message : 'has connected'
      } );
      return false;
    })


    $('#myForm').submit(function(e){
        msg = ($('#bottomBar').val());
        socket.emit( 'my event', {
          user_name : username,
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
