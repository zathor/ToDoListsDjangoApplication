from whatToDoNow.models import EndUser, ToDoList, Task, Tag
from django.shortcuts import get_object_or_404
from django.template import loader

def add_to_do_list(request):
	end_user = get_object_or_404(EndUser, user=request.user)
	list_name = request.POST['value']
	return end_user.add_to_do_list(list_name)

def add_task(request):
	to_do_list_id = request.POST['parent_pk']
	to_do_list = get_object_or_404(ToDoList, pk=to_do_list_id)
	task_name = request.POST['value']
	return to_do_list.add_task(task_name)

add_funcs = {
	"ToDoList":add_to_do_list,
	"Task":add_task
}

def remove_to_do_list(request):
	to_do_list_id = request.POST['pk']
	to_do_list = get_object_or_404(ToDoList, pk=to_do_list_id)
	try:
		to_do_list.delete()
	except:
		return False
	return True

def remove_task(request):
	task_id = request.POST['pk']
	task = get_object_or_404(Task, pk=task_id)
	try:
		task.delete()
	except:
		return False
	return True

remove_funcs = {
	"ToDoList":remove_to_do_list,
	"Task":remove_task
}

def edit_to_do_list(request):
	to_do_list_id = request.POST['pk']
	to_do_list = get_object_or_404(ToDoList, pk=to_do_list_id)
	list_name = request.POST['value']
	return to_do_list.edit(list_name)

def edit_task(request):
	task_id = request.POST['pk']
	task = get_object_or_404(Task, pk=task_id)
	task_name = request.POST['value']
	return task.edit(task_name)

def edit_tags(request):
	task_id = request.POST['parent_pk']
	task = get_object_or_404(Task, pk=task_id)
	tag_list = request.POST['value'].split(",")	
	tag_list = [task.add_tag(tag.strip()) for tag in tag_list]
	task_tag_list = task.tag_set.all()
	return [tag for tag in task_tag_list if (not tag in tag_list) and (not task.remove_tag(tag))]

edit_funcs = {
	"ToDoList": edit_to_do_list,
	"Task": edit_task,
	"Tag": edit_tags
}

def update_task_status(request):
	task_id = request.POST['pk']
	task = get_object_or_404(Task, pk=task_id)
	task_status = request.POST['status']
	return task.update_status(task_status)

update_funcs = {
	"Task": {
		"status": update_task_status
	}
}

def get_to_do_list_progress(request):
	to_do_list_id = request.POST['pk']
	to_do_list = get_object_or_404(ToDoList,pk=to_do_list_id)
	return to_do_list.progress()

get_funcs = {
	"ToDoList": {
		"progress": get_to_do_list_progress
	}
}

def add(request):
	return add_funcs[request.POST['model']](request)

def remove(request):
	return remove_funcs[request.POST['model']](request)

def edit(request):
	return edit_funcs[request.POST['model']](request)

def update(request):
	return update_funcs[request.POST['model']][request.POST['field']](request)

def get(request):
	return get_funcs[request.POST['model']][request.POST['need']](request)

add_ajax = {
	"ToDoList": {
		"template_name": "todo_list.html",
		"variable_name": "list"
	},
	"Task": {
		"template_name": "task.html",
		"variable_name": "task"
	}
}

def ajax_result_add(request,result):
	c = {
		add_ajax[request.POST['model']]["variable_name"]: result
	}
	return loader.render_to_string(add_ajax[request.POST['model']]["template_name"],c)

def ajax_result_remove(request,result):
	return str(result)

def ajax_result_edit(request,result):
	return ""

def ajax_result_update(request,result):
	if result != False:
		return str(result.to_do_list.progress())
	return str(result)

def ajax_result_get(request,result):
	return str(result)