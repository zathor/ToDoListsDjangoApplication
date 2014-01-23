function getCookie(name) {
	var cookieValue = null;
	if (document.cookie && document.cookie != '') {
		var cookies = document.cookie.split(';');
		for (var i = 0; i < cookies.length; i++) {
			var cookie = jQuery.trim(cookies[i]);
			// Does this cookie string begin with the name we want?
			if (cookie.substring(0, name.length + 1) == (name + '=')) {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue;
}

var options = {
	type: "text",
	url: url_process_operation,
	params: function(params) {
		//originally params contain pk, name and value
		delete params['name'];
		params.operation = 'edit';
		if(typeof $(this).attr('data-parent-pk') !== 'undefined') {
			params.parent_pk = $(this).attr('data-parent-pk');
		}
		params.model = $(this).attr('data-model');
		return params;
	}
};

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
// these HTTP methods do not require CSRF protection
	return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.fn.editable.defaults.mode = 'inline';

$.ajaxSetup({
	crossDomain: false,
	beforeSend: function(xhr, settings) {
		if (!csrfSafeMethod(settings.type)) {
			xhr.setRequestHeader("X-CSRFToken", csrftoken);
		}
	}
});

function add_item(value,model,parent_pk){
	if(value !== ""){
		var request = {
			type: 'POST',
			url: url_process_operation,
			data: {
				operation: "add",
				model: model,
				value: value
			},
			success: function(result){
				var container;
				if(model === "Task"){
					container = $('#tasks-'+parent_pk);
					request_progress(parent_pk);
				}
				else{
					container = $('#todolists');
				}
				container.append(result);
				$('.editable').editable(options);
				$('.addItem-input').keypress(function(event) {
					if (event.keyCode == 13 && $(this).val() !== "") {
						var val = $(this).val();
						$(this).val("");
						add_item(val,$(this).attr('data-model'),$(this).attr('data-parent-pk'));
					}
				});
				$('.statusButton').click(function() {
					var me = $(this);
					if(!me.hasClass('btn-primary')){
						update_task_status(me.val(),me.attr('data-pk'),me.attr('data-parent-pk'));
					}
				});
			}
		};
		if(model === "Task"){
			request.data.parent_pk = parent_pk;
		}
		$.ajax(request);
	}
}

function request_progress(pk){
	var request = {
		type: 'POST',
		url: url_process_operation,
		data: {
			operation: "get",
			model: "ToDoList",
			pk: pk,
			need: "progress"
		},
		success: function(result){
			var element;
			if(result !== "False"){
				$('#progress-bar-list-'+pk).css("width",result+"%");
			}
		}
	};
	$.ajax(request);
}

function remove_item(pk,model,parent_pk){
	var request = {
		type: 'POST',
		url: url_process_operation,
		data: {
			operation: "remove",
			model: model,
			pk: pk
		},
		success: function(result){
			var element;
			if(result === "True"){
				if(model === "Task"){
					element = $('#task-'+pk);
					request_progress(parent_pk);
				}
				else{
					element = $('#todolist-'+pk);
				}
				element.remove();
			}
		}
	};
	$.ajax(request);
}

function update_task_status(status,pk,parent_pk){
	var request = {
		type: 'POST',
		url: url_process_operation,
		data: {
			operation: "update",
			model: "Task",
			field: "status",
			status: status,
			pk: pk
		},
		success: function(result){
			var element;
			if(result !== "False"){
				$("#status-task-"+pk).children().each(function(){
					if($(this).hasClass('btn-primary')){
						$(this).removeClass('btn-primary');
					}
					else if($(this).val() == status){
						$(this).addClass('btn-primary');
					}
				});
				$('#progress-bar-list-'+parent_pk).css("width",result+"%");
			}
		}
	};
	$.ajax(request);
}

$(document).ready(function() {
	$('.editable').editable(options);

	$('.addItem-input').keypress(function(event) {
		if (event.keyCode == 13 && $(this).val() !== "") {
			var val = $(this).val();
			$(this).val("");
			add_item(val,$(this).attr('data-model'),$(this).attr('data-parent-pk'));
		}
	});

	$('.statusButton').click(function() {
		var me = $(this);
		if(!me.hasClass('btn-primary')){
			update_task_status(me.val(),me.attr('data-pk'),me.attr('data-parent-pk'));
		}
	});
});

$(function(){
	$(".alert-message").alert();
	$('#mainForm').submit(function(){
		$('#submit').button('loading');
	})
});