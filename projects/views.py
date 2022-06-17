from django.shortcuts import render
from projects.models import Project
from .forms import ProjectForm
from django.contrib.staticfiles.storage import staticfiles_storage
from csv import reader

# Create your views here.
def project_index(request):
    projects = Project.objects.all()
    payday = 0

    context = {
        'projects': projects
    }




    return render(request, 'project_index.html', context)

def project_detail(request):
    if request.method == "GET":
        print("GETTTTT")
        # project = Project.objects.all()

#load Hacker_News Project

# REQUEST PAGE
        context = {
            # 'project': project,
            # 'hackers_list': hackers_list,
            # 'headers': headers,
            'form': ProjectForm()
        }
        return render(request, 'project_detail.html', context)
# END OF HACKER NEWS PROJECT
    # else:


        # context = {
        #     'project': project,
        #     'hackers_list': hackers_list,
        #     'headers': headers,
        #     'form': new_form
        # }
        # return render(request, 'project_detail.html', context)

# REQUEST IS POST
    else:

        # f = ProjectForm(request.POST)
        # p = Project.objects.get(pk=f.id)


        print("POST")
        selected_project = request.POST.get("select_project")
        if selected_project == "":
            context = {
                # 'project': project,
                # 'apps_data': apps_data
                'form': ProjectForm()
            }
            return render(request, 'project_detail.html', context)
        project = Project.objects.get(pk=selected_project)

        opened_file = open('projects/static/csv/hacker_news.csv')
        read_file = reader(opened_file)
        hn = list(read_file)
        headers = hn[0]
        hn = hn[1:20]
        hackers_list = zip(hn)

# How many Ask, Show and Other posts are there
        ask_posts = []
        show_posts = []
        other_posts = []
        for row in hn:
            title = row[1].lower()
            if title.startswith('ask hn'):
                ask_posts.append(row)
            elif title.startswith('show hn'):
                show_posts.append(row)
            else:
                other_posts.append(row)

        print('Ask Posts : ' + str(len(ask_posts)))
        print('Show Posts : ' + str(len(show_posts)))
        print('Other Posts : ' + str(len(other_posts)))
# -------------------------------------------------------
        total_ask_comments = 0

        for post in ask_posts:
            num_comments = int(post[4])
            total_ask_comments += num_comments

        avg_ask_comments = total_ask_comments / len(ask_posts)
        print("Average number of comments per post for Ask HN is : " + str(round(avg_ask_comments,2)))

        total_show_comments = 0

        for post in show_posts:
            num_comments = int(post[4])
            total_show_comments += num_comments

        avg_show_comments = total_show_comments / len(show_posts)
        print("Average number of comments per post for Show HN is : " + str(round(avg_show_comments,2)))

# -------------------------------------------------------------------------

        import datetime as dt

        result_list = []

        for row in ask_posts:
            created_at = row[6]
            num_comments = int(row[4])
            result_list.append([created_at,num_comments])

        counts_by_hour = {}
        comments_by_hour = {}

        for r in result_list:
            hour = r[0]
            dt_object = dt.datetime.strptime(hour,"%m/%d/%Y %H:%M")
            dt_string = dt_object.strftime("%H")

            if dt_string not in counts_by_hour:
                counts_by_hour[dt_string] = 1
                comments_by_hour[dt_string] = r[1]
            else:
                counts_by_hour[dt_string] += 1
                comments_by_hour[dt_string] += r[1]

# -------------------------------------------------------------------------

        avg_by_hour = []

        for (cou_h1,cou_h2), (com_h1,com_h2) in zip(counts_by_hour.items(), comments_by_hour.items()):
            if cou_h1 == com_h1:
                avg_by_hour.append([cou_h1,round(com_h2 / cou_h2,2)])
            else:
                break

        print(avg_by_hour)

# -------------------------------------------------------------------------

        swap_avg_by_hour = []

        for row in avg_by_hour:
            swap_avg_by_hour.append([row[1],row[0]])

        print(swap_avg_by_hour)

# -------------------------------------------------------------------------
        sorted_swap = sorted(swap_avg_by_hour,reverse=True)

        print("Top 5 Hours for Ask Posts Comments :")

        for avg,hour in sorted_swap[:5]:
            dt_object = dt.datetime.strptime(hour,"%H")
            dt_string = dt_object.strftime("%H:%M")
            print("{time}: {comm:.2f} average comments per post".format(time=dt_string,comm=avg))

        context = {
            'project': project,
            # 'apps_data': apps_data
            'form': ProjectForm(request.POST)
        }
        return render(request, 'project_detail.html', context)
