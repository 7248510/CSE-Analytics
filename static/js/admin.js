var ip;

function init() {
  if( /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ) {
    window.location.href="mobile";
  }
    if ( $.cookie("ip") != null ) {
      ip = $.cookie("ip");
      // $.removeCookie("ip");
    }
  //   window.RTCPeerConnection = window.RTCPeerConnection || window.mozRTCPeerConnection || window.webkitRTCPeerConnection;//compatibility for Firefox and chrome
  //   var pc = new RTCPeerConnection({iceServers:[]}), noop = function(){};
  //   pc.createDataChannel('');//create a bogus data channel
  //   pc.createOffer(pc.setLocalDescription.bind(pc), noop);// create offer and set local description
  //   pc.onicecandidate = function(ice, ip)
  //   {
  //    if (ice && ice.candidate && ice.candidate.candidate)
  //    {
  //     ip = /([0-9]{1,3}(\.[0-9]{1,3}){3})/.exec(ice.candidate.candidate)[1];
  //     // window.location.href = '/users?ip=' + ip;
  //     adminIp = '10.96.4.60';
  //     if (ip == adminIp){
  //       console.log('test');
  //       // window.location.href = "/home";
  //     }else{
  //       window.location.href = "/";
  //     }
  //   }
  // }
    // Clear forms here
    // document.getElementById("file").value = "";
    // val = document.getElementById('ipadd').innerHTML + ip;
    // document.getElementById("ipadd").innerHTML = val;
    // Clear forms here
    // document.getElementById("file").value = "";
    // val = document.getElementById('ipadd').innerHTML + ip;
    // document.getElementById("ipadd").innerHTML = val;
}
function users() {
    window.RTCPeerConnection = window.RTCPeerConnection || window.mozRTCPeerConnection || window.webkitRTCPeerConnection;//compatibility for Firefox and chrome
    var pc = new RTCPeerConnection({iceServers:[]}), noop = function(){};
    pc.createDataChannel('');//create a bogus data channel
    pc.createOffer(pc.setLocalDescription.bind(pc), noop);// create offer and set local description
    pc.onicecandidate = function(ice, ip)
    {
     if (ice && ice.candidate && ice.candidate.candidate)
     {
      ip = /([0-9]{1,3}(\.[0-9]{1,3}){3})/.exec(ice.candidate.candidate)[1];
      window.location.href = '/users?ip=' + ip;
    }
    // Clear forms here
    // document.getElementById("file").value = "";
    // val = document.getElementById('ipadd').innerHTML + ip;
    // document.getElementById("ipadd").innerHTML = val;
}
}
    var socket = io.connect("http://" + document.domain)
window.onload = init;
function stream(){
  window.location.href = "http://" + ip + "/streaming";
}
function showFile(){
  filename = document.getElementById('file').files.item(0).name;
  document.getElementById('filespan').innerHTML = filename;
}
function results(){
  var url = "/scanResults?ip=" + ip;
  window.location.href=url;
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
