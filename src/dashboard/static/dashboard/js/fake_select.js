/*************************************************** EXECUTABLE CODE */

$(document).ready(function () {
	const body = document.querySelector('body');
	$(".fake_select").click(handleFilterSelectDropdownClick);

	body.addEventListener('click', handleBodyClick)

	function handleBodyClick(e) {
		let hasOpenedFakeSelect = document.querySelector('.single_filter.active');
        
        if (hasOpenedFakeSelect && e.target.closest('.options') == null && e.target.closest('.single_filter.active') == null) {
            // hasOpenedFakeSelect.classList.remove('active');
			handleFilterSelectDropdownClick(e);
        }
	}
});

/*************************************************** DECLARATIONS */

function handleFilterSelectDropdownClick(event) {
	event.preventDefault();
	let $this = $(this);
	if (!$this.hasClass("active")) {
		$("#filter_menu .fake_select").removeClass("active").parent().removeClass("active");
		$this.addClass("active");
		$this.parent().addClass("active");
	} else {
		$this.removeClass("active");
		$this.parent().removeClass("active");
	}
}