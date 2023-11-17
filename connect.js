$("#answer-form").on("submit", function(event){
  event.preventDefault();
  var new_answer = $("#answer-input").val();
  if (new_answer && new_answer.toLowerCase() != 'saltar') {
  $.post("/update_knowledge_base", {user_input: user_input, new_answer: new_answer}, function(data){
    $("#chat-container").append("<div class='bot-message'>" + data.response + "</div>");
  });
  }
 });
 