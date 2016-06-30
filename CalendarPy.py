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
    return months[Month-1]

def MaxFont(draw,text,rect,mono=False):
    Font="arial.ttf"
    if mono: 
        Font="cour.ttf"
        #Font="courbd.ttf"
    #print(text)
    #print(rect)
    i=1
    font=ImageFont.truetype(Font,i)
    #font=ImageFont.truetype(,i)
    while (draw.textsize(text,font)[0]<(rect[2]-rect[0]) and
           draw.textsize(text,font)[1]<(rect[3]-rect[1])):
        i+=1
        font=ImageFont.truetype(Font,i)
        #print(draw.textsize(text,font))
        #print(i)

    if font.size>3:
        font=ImageFont.truetype(Font,i)
    return font

def GetCentered(draw,text,font,rect):
    W=rect[2]-rect[0]
    H=rect[3]-rect[1]
    w,h=draw.textsize(text,font)
    return ( rect[0]+(W-w)//2,rect[1]+(H-h)//2 )

#Make rectangle on pixel smaller
def Shrink(rectangle):
    return (rectangle[0]+1,rectangle[1]+1,
            rectangle[2]-1,rectangle[3]-1)

#Draw thinker boardered rectangle
def DrawRectangle(draw,rectangle,width=1):
    for i in range(width):
        draw.rectangle(rectangle,outline=(0,0,0))
        rectangle=Shrink(rectangle)


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
    PrevSmallCalendarRect = (2*Margin, Margin, 2*Margin+ Header + Margin - HeaderCellHeight, Header + Margin - HeaderCellHeight)
    smallPrevBegin=PrevSmallCalendarRect[:2]
    
    if month==1:
        smallPrev=calendar.TextCalendar(6).formatmonth(year-1,12)
    else:
        smallPrev=calendar.TextCalendar(6).formatmonth(year,month-1)
    font=MaxFont(draw,smallPrev,PrevSmallCalendarRect,True)
    draw.text(smallPrevBegin,smallPrev,(0,0,0),font=font)

    #Draw small next month
    NextSmallCalendarRect = [x for x in PrevSmallCalendarRect]
    NextSmallCalendarRect[0]=Width-2*Margin-(PrevSmallCalendarRect[2]-PrevSmallCalendarRect[0])
    NextSmallCalendarRect[2]=Width-2*Margin
    smallNextBegin=NextSmallCalendarRect[:2]
    
    if month==12:
        smallNext=calendar.TextCalendar(6).formatmonth(year+1,1)
    else:
        smallNext=calendar.TextCalendar(6).formatmonth(year,month+1)
    font=MaxFont(draw,smallNext,NextSmallCalendarRect,True)
    draw.text(smallNextBegin,smallNext,(0,0,0),font=font)

    #draw.rectangle(PrevSmallCalendarRect,outline=(0,0,0))
    #draw.rectangle(NextSmallCalendarRect,outline=(0,0,0))


    #Draw day labels
    Padding=int(HeaderCellWidth*.05)
    DaysLabelRect = (Margin + HeaderCellWidth * 3+Padding, Header + Margin - HeaderCellHeight+Padding, Margin + HeaderCellWidth * 3 + HeaderCellWidth -Padding, Header + Margin - HeaderCellHeight + HeaderCellHeight-Padding)
    font=MaxFont(draw,DayText(3),DaysLabelRect)
    
    for Day in range(7):
        DaysLabelRect = (Margin + HeaderCellWidth * Day, Header + Margin - HeaderCellHeight, Margin + HeaderCellWidth * Day + HeaderCellWidth, Header + Margin - HeaderCellHeight + HeaderCellHeight)
        DaysTextLabelRect=[DaysLabelRect[0]+Padding,DaysLabelRect[1]+Padding,DaysLabelRect[2]-Padding,DaysLabelRect[3]-Padding]

        #draw.rectangle(DaysLabelRect,outline=(0,0,0))
        DrawRectangle(draw,DaysLabelRect,3)
        draw.text(GetCentered(draw,DayText(Day),font,DaysTextLabelRect),DayText(Day),(0,0,0),font=font)
        


    Days=calendar.Calendar(6).monthdayscalendar(year,month)

    Weeks=len(Days)
    CellWidth = (Width - 2 * Margin) // 7
    CellHeight = (Height - 2 * Margin-Header) // Weeks
    Padding=int(CellWidth*.05)
    for week in range(Weeks):
        for Day in range(7):
            DaysRect = (Margin + CellWidth * Day, Header + Margin+CellHeight*week, Margin + CellWidth * Day + CellWidth, Header + Margin+CellHeight*week + CellHeight)
            #draw.rectangle(DaysRect,outline=(0,0,0))
            DrawRectangle(draw,DaysRect,3)
            DaysTextRect = [x+Padding for x in DaysRect]

            if Days[week][Day]>0:
                draw.text(DaysTextRect,str(Days[week][Day]),(0,0,0),font=font)


    #Draw Header
    Padding=int(Width*.05)
    HeaderText=MonthText(month)+" " + str(year)
    #HeaderRect = (Margin, Margin, Margin + Width - 2 * Margin, Margin + Header - HeaderCellHeight)
    HeaderRect = (PrevSmallCalendarRect[2]+Padding,PrevSmallCalendarRect[1],NextSmallCalendarRect[0]-Padding,NextSmallCalendarRect[3])

    font=MaxFont(draw,HeaderText,HeaderRect)
    draw.text(GetCentered(draw,HeaderText,font,HeaderRect),HeaderText,(0,0,0),font=font)
    #draw.rectangle(HeaderRect,outline=(0,0,0))


    cal.save(str(year)+"-" + str(month) +".png")
    #cal.show()

if __name__ == "__main__":
    #for i in range(1,13):
        #print(i,calendar.Calendar(6).monthdayscalendar(2016,i))
    #print(calendar.TextCalendar(6).formatmonth(2016,2))
    
    for m in range(1,13):
        print(m)
        Calendar(2016,m)
    #today=datetime.datetime.now()
    #Calendar(today.year,today.month)