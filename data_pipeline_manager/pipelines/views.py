from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from .forms import OCR_ENGINES, OCR_MODELS, OCRTaskForm
from .models import BatchTask, PipelineTypes, Task


def dashboard(request):
    if request.method == "POST":
        form = OCRTaskForm(request.POST)
        if form.is_valid():
            batch = BatchTask.objects.create(
                inputs=form.cleaned_data["inputs"],
                name=form.cleaned_data["name"],
                pipeline_type=PipelineTypes.IMPORT,
                pipeline_config={
                    "ocr_engine": OCR_ENGINES[form.cleaned_data["ocr_engine"]],
                    "model_name": OCR_MODELS[form.cleaned_data["model_name"]],
                },
            )
            batch.run()
            return HttpResponseRedirect(reverse_lazy("pipelines:dashboard"))
    else:
        form = OCRTaskForm()

    latest_ten_batches = BatchTask.objects.order_by("-started_on")[:10]
    context = {"form": form, "batch_tasks": latest_ten_batches}

    return render(request, "pipelines/dashboard.html", context=context)


class BatchTaskListView(generic.ListView):
    model = BatchTask
    paginate_by = 10
    template_name = "pipelines/batch_task_lists.html"
    context_object_name = "batch_tasks"


batch_task_list_view = BatchTaskListView.as_view()


class BatchTaskDetailView(generic.DetailView):
    model = BatchTask
    template_name = "pipelines/batch_task_detail.html"
    context_object_name = "batch"


batch_task_detail_view = BatchTaskDetailView.as_view()


class TaskDetailView(generic.DetailView):
    model = Task
    template_name = "pipelines/task_detail.html"
    context_object_name = "task"


task_detail_view = TaskDetailView.as_view()