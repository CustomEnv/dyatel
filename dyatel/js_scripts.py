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

check_element_js = 'arguments[0].checked = true'
uncheck_element_js = 'arguments[0].checked = false'
is_element_checked_js = 'return arguments[0].checked'
