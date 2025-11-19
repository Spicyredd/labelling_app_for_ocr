# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import ValidLabelPair, RemovedLabelPair
from .forms import LabelEditForm
from django.core.paginator import Paginator
from django.conf import settings
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import ValidLabelPair, RemovedLabelPair

def valid_labels(request):
    # --- GET request logic (filtering and initial page load) ---
    status_filter = request.GET.get("status", "")  # Get status from URL
    queryset = ValidLabelPair.objects.all().order_by("id") # Start with a predictable order

    if status_filter in ["valid", "not_checked"]:
        queryset = queryset.filter(label_status=status_filter)

    # --- POST request logic (handling form submissions) ---
    if request.method == "POST":
        row_action = request.POST.get("row_action")
        bulk_action = request.POST.get("bulk_action")

        if row_action:
            if row_action.startswith("update_single_"):
                obj_id = row_action.replace("update_single_", "")
                obj = get_object_or_404(ValidLabelPair, id=obj_id)
                obj.label = request.POST.get(f"label_{obj_id}", obj.label)
                obj.label_status = request.POST.get(f"status_{obj_id}", obj.label_status)
                obj.save()

            elif row_action.startswith("remove_single_"):
                obj_id = row_action.replace("remove_single_", "")
                obj = get_object_or_404(ValidLabelPair, id=obj_id)
                RemovedLabelPair.objects.create(
                    label=obj.label,
                    image_path=obj.image_path,
                    removed_reason="Removed manually"
                )
                obj.delete()
            
        elif bulk_action:
            selected_ids = request.POST.getlist("selected")
            items = ValidLabelPair.objects.filter(id__in=selected_ids)
    
            if bulk_action == "bulk_update":
                new_status = request.POST.get("new_status", "not_checked")
                items.update(label_status=new_status) 
    
            elif bulk_action == "bulk_remove":
                reason = request.POST.get("removed_reason", "Removed in bulk")
                for obj in items:
                    RemovedLabelPair.objects.create(
                        label=obj.label,
                        image_path=obj.image_path,
                        removed_reason=reason
                    )
                items.delete()

        # --- THE FIX ---
        # Instead of redirecting to request.path, we build the full URL with filters.
        query_params = request.GET.urlencode()
        redirect_url = request.path
        if query_params:
            redirect_url = f"{redirect_url}?{query_params}"
            
        return redirect(redirect_url)

    # --- Final step for GET requests: Pagination ---
    paginator = Paginator(queryset, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "labelmanager/valid_labels.html", {
        "page_obj": page_obj,
        "MEDIA_URL": settings.MEDIA_URL,
        "status_filter": status_filter,
    })

def label_list(request):
    # --- Bulk Actions ---
    if request.method == "POST":
        selected_ids = request.POST.getlist("selected")
        action = request.POST.get("action")

        if selected_ids and action:
            items = ValidLabelPair.objects.filter(id__in=selected_ids)

            if action == "mark_valid":
                items.update(label_status="valid")

            elif action == "mark_not_checked":
                items.update(label_status="not_checked")

            elif action == "remove":
                reason = request.POST.get("bulk_reason", "Removed in bulk")
                for item in items:
                    RemovedLabelPair.objects.create(
                        label=item.label,
                        image_path=item.image_path,
                        removed_reason=reason
                    )
                items.delete()

        return redirect("label_list")

    # --- Pagination ---
    items = ValidLabelPair.objects.all().order_by("id")
    paginator = Paginator(items, 15)  # show 15 rows per page

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "labelmanager/label_list.html", {
        "page_obj": page_obj,
        "MEDIA_URL": settings.MEDIA_URL
    })
def edit_label(request, pk):
    label_obj = get_object_or_404(ValidLabelPair, pk=pk)

    if request.method == 'POST':
        form = LabelEditForm(request.POST, instance=label_obj)
        if form.is_valid():
            form.save()
            return redirect('label_list')
    else:
        form = LabelEditForm(instance=label_obj)

    return render(request, 'labelmanager/edit_label.html', {'form': form, 'label_obj': label_obj})


def remove_label(request, pk):
    label_obj = get_object_or_404(ValidLabelPair, pk=pk)

    if request.method == 'POST':
        reason = request.POST.get('reason')
        RemovedLabelPair.objects.create(
            label=label_obj.label,
            image_path=label_obj.image_path,
            removed_reason=reason
        )
        label_obj.delete()
        return redirect('label_list')

    return render(request, 'labelmanager/remove_label.html', {'label': label_obj})