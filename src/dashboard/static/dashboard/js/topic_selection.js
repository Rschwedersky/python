/*************************************************** EXECUTABLE CODE */

$(document).ready(function () {
	$("#root").on("click", ".topic_selection .topic_header", handleConfigTopicSelection);
});

/*************************************************** DECLARATIONS */

function handleConfigTopicSelection() {
	$(this).parent().toggleClass("opened");
}
