function find_new_thread(){
  var threads = document.getElementsByClassName('thread');

  for ( var i = 0 ; i < threads.length ; i ++ ){
    var thread = threads[i];
    var links = thread.getElementsByTagName('a');

    if (links.length != 1){
      continue;
    }

    href = links[0].getAttribute('href');

    if (!href){
      continue;
    }

    if (!localStorage.getItem(href)){
      thread.className = thread.className + " new";
    }
  }
}

function hover_in(event) {
  this.className = this.className + " hover";
}

function hover_out(event) {
  this.className = this.className.replace(' hover','');
}

function set_visited(event) {
  this.className = this.className.replace('new', '');

  links = this.getElementsByTagName('a');
  if (links.length != 1){
    return true;
  }
  href = links[0].getAttribute('href');
  if (!href){
    return true;
  } 
  localStorage.setItem(href, 1);
}

function set_nav_active( index ) {
    nav_items = document.getElementById('nav').getElementsByTagName('a');
    for (var i = 0; i< nav_items.length; i++) {
      nav_items[i].className = "";
    }
    nav_items[index].className = 'active';
}


function goto (position) {

    var nav = document.getElementById('nav');
    var links = nav.getElementsByTagName('a');
    
    // Set default page to index 0;
    var where = 0; 

    for ( var i = 0; i < links.length; i++ ){
      if (window.location.pathname == encodeURI(links[i].getAttribute('href'))){
        where = i; 
        break;
      }
    }
   
    where += position;

    if (where >= links.length){
      where = 0;
    }
    else if(where < 0){
      where = links.length - 1;
    }

    window.location.href = links[where].getAttribute('href');

  }


function on_load (){

  var panel = document.getElementById('panel');

  var max_with = 100;
  var to_left = document.getElementById('to_left'); 
  var to_right = document.getElementById('to_right');
  var direction = 0; // 1 goto right, -1 goto left;
  var threshold = 30; // px

  function onTouchStart (event) {
    this.start_x = event.touches[0].clientX;
    this.start_y = event.touches[0].clientY;
  }

  function onTouchEnd (event) {
    to_left.style.width = "0px";
    to_right.style.width = "0px";
    if (direction != 0){
      if (Math.abs(this.delta_x) > max_with){
        goto(direction);
      }
    }
  }

  function onTouchMove (event) {
    this.end_x = event.touches[0].clientX;
    this.end_y = event.touches[0].clientY;
    this.delta_x = this.end_x - this.start_x;
    this.delta_y = this.end_y - this.start_y;
    
    if (Math.abs(this.delta_x) > threshold ){

      grow = Math.abs(this.delta_x) - threshold + "px";
      if (this.delta_x > 0 & Math.abs(this.delta_x) < max_with) {
        /* swipe right */
        to_left.style.width = grow;
        direction = -1;
      }

      else if (this.delta_x < 0 & Math.abs(this.delta_x) < max_with) {
        /* swipe left */
        to_right.style.width = grow;
        direction = 1;
      }
    }
  }

  panel.addEventListener("touchstart", onTouchStart, false);
  panel.addEventListener("touchend", onTouchEnd, false);
  panel.addEventListener("touchmove", onTouchMove, false);

  find_new_thread();

  threads = document.getElementsByClassName('thread');
  for ( var i = 0 ; i < threads.length ; i ++ ){
    var thread = threads[i];
    thread.addEventListener("touchstart", hover_in, false);
    thread.addEventListener("touchend", hover_out, false);
    thread.addEventListener("touchend", set_visited, false);
  }
}
