scroll_into_view_blocks = ('start', 'center', 'end', 'nearest')
get_inner_height_js = 'return window.innerHeight'
get_inner_width_js = 'return window.innerWidth'

get_element_position_on_screen_js = """
function getPositionOnScreen(elem) {
  let box = elem.getBoundingClientRect();
  var y;
  var x;
  y = Math.floor(box.top)
  x = Math.floor(box.left)
  return {
    x: x,
    y: y
  };
};
return getPositionOnScreen(arguments[0])
"""

get_element_size_js = """
function getSize(elem) {
  let box = elem.getBoundingClientRect();
  var width;
  var height;
  width = Math.floor(box.width)
  height = Math.floor(box.height)
  return {
    width: width,
    height: height
  };
};
return getSize(arguments[0])
"""

delete_element_over_js = """
const elements = document.getElementsByClassName("dyatel-visual-comparison-support-element");

for (var i=0, max=elements.length; i < max; i++) {
     elements[0].remove()
};
"""

add_element_over_js = """
function appendElement(given_obj) {
    given_obj = given_obj.getBoundingClientRect();
    dyatel_obj = document.createElement("div");

    dyatel_obj.style.zIndex=9999999;
    dyatel_obj.setAttribute("class","dyatel-visual-comparison-support-element");
    document.body.appendChild(dyatel_obj);

    dyatel_obj.style.position = "fixed";
    dyatel_obj.style.backgroundColor = "#000";

    dyatel_obj.style.width = given_obj.width + "px";
    dyatel_obj.style.height = given_obj.height + "px";
    dyatel_obj.style.top = given_obj.y + "px";
    dyatel_obj.style.left = given_obj.x + "px";
};

return appendElement(arguments[0]);
"""


add_driver_index_comment_js = """
function addComment(driver_index) {
  comment = document.createComment(" " + driver_index + " ");
  document.body.appendChild(comment);
};

addComment(arguments[0])
"""

find_comments_js = """
function filterNone() {
    return NodeFilter.FILTER_ACCEPT;
}

function getAllComments(rootElem) {
    var comments = [];
    // Fourth argument, which is actually obsolete according to the DOM4 standard, is required in IE 11
    var iterator = document.createNodeIterator(rootElem, NodeFilter.SHOW_COMMENT, filterNone, false);
    var curNode;
    while (curNode = iterator.nextNode()) {
        comments.push(curNode.nodeValue);
    }
    return comments;
}

return getAllComments(document.body);
"""

trigger_react = """
function reactTriggerChange(node) {
  var supportedInputTypes = {
    color: true,
    date: true,
    datetime: true,
    'datetime-local': true,
    email: true,
    month: true,
    number: true,
    password: true,
    range: true,
    search: true,
    tel: true,
    text: true,
    time: true,
    url: true,
    week: true
  };
  var nodeName = node.nodeName.toLowerCase();
  var type = node.type;
  var event;
  var descriptor;
  var initialValue;
  var initialChecked;
  var initialCheckedRadio;
  function deletePropertySafe(elem, prop) {
    var desc = Object.getOwnPropertyDescriptor(elem, prop);
    if (desc && desc.configurable) {
      delete elem[prop];
    }
  }
  function changeRangeValue(range) {
    var initMin = range.min;
    var initMax = range.max;
    var initStep = range.step;
    var initVal = Number(range.value);
    range.min = initVal;
    range.max = initVal + 1;
    range.step = 1;
    range.value = initVal + 1;
    deletePropertySafe(range, 'value');
    range.min = initMin;
    range.max = initMax;
    range.step = initStep;
    range.value = initVal;
  }
  function getCheckedRadio(radio) {
    var name = radio.name;
    var radios;
    var i;
    if (name) {
      radios = document.querySelectorAll('input[type="radio"][name="' + name + '"]');
      for (i = 0; i < radios.length; i += 1) {
        if (radios[i].checked) {
          return radios[i] !== radio ? radios[i] : null;
        }
      }
    }
    return null;
  }
  function preventChecking(e) {
    e.preventDefault();
    if (!initialChecked) {
      e.target.checked = false;
    }
    if (initialCheckedRadio) {
      initialCheckedRadio.checked = true;
    }
  }
  if (nodeName === 'select' ||
    (nodeName === 'input' && type === 'file')) {
    event = document.createEvent('HTMLEvents');
    event.initEvent('change', true, false);
    node.dispatchEvent(event);
  } else if ((nodeName === 'input' && supportedInputTypes[type]) ||
    nodeName === 'textarea') {
    descriptor = Object.getOwnPropertyDescriptor(node, 'value');
    event = document.createEvent('UIEvents');
    event.initEvent('focus', false, false);
    node.dispatchEvent(event);
    if (type === 'range') {
      changeRangeValue(node);
    } else {
      initialValue = node.value;
      node.value = initialValue + '#';
      deletePropertySafe(node, 'value');
      node.value = initialValue;
    }
    event = document.createEvent('HTMLEvents');
    event.initEvent('propertychange', false, false);
    event.propertyName = 'value';
    node.dispatchEvent(event);
    event = document.createEvent('HTMLEvents');
    event.initEvent('input', true, false);
    node.dispatchEvent(event);
    if (descriptor) {
      Object.defineProperty(node, 'value', descriptor);
    }
  } else if (nodeName === 'input' && type === 'checkbox') {
    node.checked = !node.checked;
    event = document.createEvent('MouseEvents');
    event.initEvent('click', true, true);
    node.dispatchEvent(event);
  } else if (nodeName === 'input' && type === 'radio') {
    initialChecked = node.checked;
    initialCheckedRadio = getCheckedRadio(node);
    descriptor = Object.getOwnPropertyDescriptor(node, 'checked');
    node.checked = !initialChecked;
    deletePropertySafe(node, 'checked');
    node.checked = initialChecked;
    node.addEventListener('click', preventChecking, true);
    event = document.createEvent('MouseEvents');
    event.initEvent('click', true, true);
    node.dispatchEvent(event);
    node.removeEventListener('click', preventChecking, true);
    if (descriptor) {
      Object.defineProperty(node, 'checked', descriptor);
    }
  }
};
reactTriggerChange(arguments[0]);
"""
