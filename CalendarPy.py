import datetime
import calendar
from PIL import Image #pip install pillow
from PIL import ImageDraw
from PIL import ImageFont

def DayText(Day):
    days = [ "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday" ]
    return days[Day]

def MonthText(Month):
    months =["January","February","March","April","May","June", "July","August","September","October","November","December"]
    return months[Month]

def MaxFont(draw,text,rect):
    i=1
    font=ImageFont.truetype("arial.ttf",i)
    while (draw.textsize(text,font)[0]<rect[2]-rect[0] and
           draw.textsize(text,font)[1]<rect[3]-rect[1]):
        i+=1
        font=ImageFont.truetype("arial.ttf",i)
        #print(i)
    font=ImageFont.truetype("arial.ttf",i-2)
    return font

def GetCentered(draw,text,font,rect):
    W=rect[2]-rect[0]
    H=rect[3]-rect[1]
    w,h=draw.textsize(text,font)
    return ( rect[0]+(W-w)//2,rect[1]+(H-h)//2 )

def Calendar(year,month):
    dpi = 300
    
    Width = int(11 * dpi)
    Height = int(8.5 * dpi)
    Margin = int(.5 * dpi)

    cal=Image.new("RGB",(Width,Height),"white")
    draw=ImageDraw.Draw(cal)
    
    Header = Height//5
    HeaderCellWidth=(Width-2*Margin)//7
    HeaderCellHeight =(Height-2*Margin)//20

    #Draw samll previous month
    PrevSmallCalendarRect = (2*Margin, Margin, Header + Margin - HeaderCellHeight, Header + Margin - HeaderCellHeight)
    smallPrevBegin=(2*Margin,Margin)
    smallPrev=calendar.TextCalendar(6).formatmonth(year,month-1)

    #i=1
    #font=ImageFont.truetype("arial.ttf",i)
    #while (draw.textsize(smallPrev,font)[0]<PrevSmallCalendarRect[2]-PrevSmallCalendarRect[0] and
    #       draw.textsize(smallPrev,font)[1]<PrevSmallCalendarRect[3]-PrevSmallCalendarRect[1]):
    #    i+=1
    #    font=ImageFont.truetype("arial.ttf",i)
    #    print(i)
    #font=ImageFont.truetype("arial.ttf",i-1)
    font=MaxFont(draw,smallPrev,PrevSmallCalendarRect)
    draw.text(smallPrevBegin,smallPrev,(0,0,0),font=font)

    #Draw small next month
    NextSmallCalendarRect = (Width-(2 * Margin+Header + Margin - HeaderCellHeight), Margin, Header + Margin - HeaderCellHeight, Header + Margin - HeaderCellHeight)
    smallNextBegin=(Width-(2 * Margin+Header + Margin - HeaderCellHeight), Margin)
    smallNext=calendar.TextCalendar(6).formatmonth(year,month+1)
    font=ImageFont.truetype("arial.ttf",20)
    draw.text(smallNextBegin,smallPrev,(0,0,0),font=font)


    #Draw day labels
    DaysLabelRect = (Margin + HeaderCellWidth * 3, Header + Margin - HeaderCellHeight, Margin + HeaderCellWidth * 3 + HeaderCellWidth, Header + Margin - HeaderCellHeight + HeaderCellHeight)
    font=MaxFont(draw,DayText(3),DaysLabelRect)
    for Day in range(7):
        DaysLabelRect = (Margin + HeaderCellWidth * Day, Header + Margin - HeaderCellHeight, Margin + HeaderCellWidth * Day + HeaderCellWidth, Header + Margin - HeaderCellHeight + HeaderCellHeight)
        draw.rectangle(DaysLabelRect,outline=(0,0,0))
        #draw.text(DaysLabelRect,DayText(Day),(0,0,0),font=font)
        draw.text(GetCentered(draw,DayText(Day),font,DaysLabelRect),DayText(Day),(0,0,0),font=font)
        


    Days=calendar.Calendar(6).monthdayscalendar(year,month)

    Weeks=len(Days)
    CellWidth = (Width - 2 * Margin) // 7
    CellHeight = (Height - 2 * Margin-Header) // Weeks
    Padding=5
    for week in range(Weeks):
        for Day in range(7):
            DaysRect = (Margin + CellWidth * Day, Header + Margin+CellHeight*week, Margin + CellWidth * Day + CellWidth, Header + Margin+CellHeight*week + CellHeight)
            draw.rectangle(DaysRect,outline=(0,0,0))
            DaysTextRect = [x+Padding for x in DaysRect]

            if Days[week][Day]>0:
                draw.text(DaysTextRect,str(Days[week][Day]),(0,0,0),font=font)


    #Draw Header
    Padding=int(Width*.1)
    HeaderText=MonthText(month)+" " + str(year)
    #HeaderRect = (Margin, Margin, Margin + Width - 2 * Margin, Margin + Header - HeaderCellHeight)
    HeaderRect = (PrevSmallCalendarRect[2]+Padding,PrevSmallCalendarRect[1],NextSmallCalendarRect[0]-Padding,NextSmallCalendarRect[3])
    print(HeaderRect)
    font=MaxFont(draw,HeaderText,HeaderRect)
    draw.text(HeaderRect,HeaderText,(0,0,0),font=font)



    cal.save("image.png")


if __name__ == "__main__":
    #for i in range(1,13):
        #print(i,calendar.Calendar(6).monthdayscalendar(2016,i))
    #print(calendar.TextCalendar(6).formatmonth(2016,2))
    Calendar(2016,2)