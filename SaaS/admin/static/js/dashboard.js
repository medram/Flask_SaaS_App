$(function(){
	//////////////////////////////////// Delete Button ////////////////////////////////////////
	$('table.activate-delete-button').on('click', (e) => {
		let selector = null
		if (e.target.tagName == 'A' && e.target.classList.contains('deletable'))
		{
			e.preventDefault()
			selector = e.target

			if (confirm('Are You sure you want to delete this item?'))
			{
				function deleteTableTr(selector)
				{
					$(selector).parents('tr').remove()
				}

				// send a delete request to the server.
				async function deleteItem(selector)
				{
					const res = await fetch(selector.href, {
						method: 'DELETE'
					})

					let data = await res.json()
					if (data.status)
					{	
						deleteTableTr(selector)
						alert(data.message)
					}
					else
						alert('Error: '+ data.error)
				}

				try {
					deleteItem(selector)
				} catch (error) {
					alert('Error: ' + error)
				}

			}
		}

	})

	//////////////////////////////////// DateTime Picker //////////////////////////////////////
	const FORMAT = "YYYY-MM-DD HH:mm:ss"
	const selector = "input[data-toggle=datetimepicker]"
	const icons = {
			time: "fa fa-clock",
			date: "fa fa-calendar",
			up: "fa fa-arrow-up",
			down: "fa fa-arrow-down"
		}

	$(selector).each((i, item) => {
		let input = $(item)

		input.datetimepicker({
			language: 'en',
			format: FORMAT,
			useCurrent: false,
			icons
			//defaultDate: "{{ field.data.date() }}",
		})
	
		// insert a default value.
		input.val(item.defaultValue)
	})

	//const input = $("#{{ "datetimepicker-" + field.name }}")



	// for datetime picker.
	$(selector).on('focus', e => {
		let input = $(e.target)
		// set the selected datetime to the input field.
		input.on("change.datetimepicker", e => {
			//e.date.format(FORMAT)
			input.val(e.date.format(FORMAT))
		})
	}) // end event
}) // end function.