from django.shortcuts import render,redirect
from records.models import Thing,Item, Tsv
from .forms import TsvModelForm
from django.contrib import messages
from datetime import datetime
from dateutil import parser
import csv
from . import literals





def upload_file_view(request):

    form = TsvModelForm(request.POST or None, request.FILES or None)
    
    
    stat_one_val = [
        literals.STAT_ONE_CHOICE_ONE,
        literals.STAT_ONE_CHOICE_TWO,
        literals.STAT_ONE_CHOICE_THREE,
        literals.STAT_ONE_CHOICE_FOUR,
        literals.STAT_ONE_CHOICE_FIVE,
        literals.STAT_ONE_CHOICE_NOT_SPECIFIED
        ]

    stat_two_val = [
        literals.STAT_TWO_CHOICE_ONE,
        literals.STAT_TWO_CHOICE_TWO,
        literals.STAT_TWO_CHOICE_THREE,
        literals.STAT_TWO_CHOICE_NOT_SPECIFIED
    ]



    if form.is_valid():
        
        p = form.save(commit=False)
        form= TsvModelForm()
    
        with open(p.file_name.path, 'r') as file:
            reader = csv.reader(file, delimiter="\t")

            Thing_list = []
            Item_list = []

            for i,row in enumerate(reader):
                if i == 0:
                    if row[0] != "code" or row[1] != "description" or row[2] != 'date' or row[3] != 'stat_one' or row[4] != 'stat_two' or row[5] != 'name' or row[6] != 'rating' or row[7] != 'score' :
                        messages.error(request,"Table schema invalid")
                        break
                    p.save()
                else:
                    code = row[0]
                    description = row[1]
                    
                    ### date Validation. Also will accept any Date format and convert it into ISO format
                    date = parser.parse(row[2])
                    date = datetime.strftime(date, '%Y-%m-%d')

                    ### Stat_one Validation
                    stat_one = row[3]
                    if stat_one not in stat_one_val:
                        messages.error(request,"Value to Stat_one is not valid in line number: " + str(i+1))
                        continue

                    ### Stat_two Validation                   
                    stat_two = row[4]
                    if stat_two not in stat_two_val:
                        messages.error(request,'Value of stat_two is not valid in line number: ' + str(i+1))
                        continue
                    name = row[5]
                    score = row[7]

                    ### Rating Validation
                    try:
                        rating = round(float(row[6]),1)
                        if rating < 1.0 or rating > 5.0 :
                            messages.error(request,"Rating not in range in line number: " + str(i+1))
                            continue
                        rating = str(rating)
                    except:
                        messages.error(request,"Rating not number in line number: " + str(i+1))     

                    ## Saving the Valid Row in database
                    thingInfo = Thing(
                        code = code,
                        description = description,
                        date = date,
                        stat_one = stat_one,
                        stat_two = stat_two
                    )
                    thingInfo.save()
                    Thing_list.append(thingInfo)
                   
                    itemInfo = Item(
                        thing = thingInfo,
                        name = name,
                        rating = rating,
                        score = score
                    )  
                    itemInfo.save()
                    Item_list.append(itemInfo)
        


        context = {
            'form' : form,
            'things' : Thing_list,
            'Items' : Item_list
        }
        

        return render(request,'tsv_upload.html', context)

    context = {
        'form' : form
    }

    return render(request,'tsv_upload.html', context)

