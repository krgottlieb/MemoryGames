"""
Rebecca Gottlieb
Memory Game
3/2020
"""
import wx, os, random, time

class MemoryGame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="Memory Game")
        self.SetSize(700,600)
        self.Move(600,250)
        self.panel = wx.Panel(self) #window that holds controls...generally in a frame

        self.makePairs = 12 #how many pairs in the game

        self.getImages = GetJpgList("./pictures")#finds a list of picutres saved in a folder
        #random.shuffle(self.getImages)#shuffles the pictures so they're not in the same order every time
        self.makeImageMatch = self.getImages[0:self.makePairs]#get the images and set them into an array
        self.makeImageMatch = self.makeImageMatch * 2#multiply array by two to make the match
        random.shuffle(self.makeImageMatch)#shuffle the array to make it random

        card = wx.Image("cardBack.jpg", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        #give the name of your file
        #wx.BITMAP_TYPE_ANY will try to autodetect the format. By adding index=-1 it will look for the 1st image
        #ConvertToBitmap will take the file and change it to a bitmap format
        self.deck = []#create an array to populate with the cards
        
        for i in range(len(self.makeImageMatch)):
            self.deck.append(wx.StaticBitmap(self.panel, wx.ID_ANY, card, name=self.makeImageMatch[i]))
            #append the deck with the pictures stored in the file given
            #StaticBitmap allows the picture to be displayed inside the panel

        for img in self.deck:
            img.Bind(wx.EVT_LEFT_DOWN, self.onClick)
            #When left click on a card it calls check function

        verticalAlignment = wx.BoxSizer(wx.VERTICAL)
        #BoxSizer allows you to set your orientation as either horizontal or vertical
        title = wx.StaticText(self.panel, label="Memory Game!!!")
        title.SetForegroundColour((255,0,127))
        font = self.GetFont()
        font.SetPointSize(30)
        title.SetFont(font)
        verticalAlignment.Add(title,proportion=2, flag=wx.ALIGN_CENTER, border=10)
        #title is being worked in, proportion gives the title the extra space, flag makes sure the components are applied
        grid = wx.GridSizer(rows = 4, cols = 6, vgap=15, hgap=15)
        #lays the children into a two-dimensional tabel
        grid.AddMany(self.deck)
        #neat trick to add subwindows into a window
        verticalAlignment.Add(grid, proportion=0, flag=wx.ALIGN_CENTER, border=10)
        #the grid is the area being worked in and flag makes sure the components are applied
        self.panel.SetSizer(verticalAlignment)
        #sets the window to have the given layout sizer

        self.foundMatches=0
        self.clickCount=0
        self.cardOne = ""
        self.totalTries = 0
        
        self.statusbar = self.CreateStatusBar(1)
        self.statusbar.SetStatusText("Total Tries:" + str(self.totalTries) + "  Total Matches:" + str(self.foundMatches))

        def playAgain(event):
            self.Close(True)
            app = wx.App(False) #adding false tells the app not to redirect errors to a new window
            frame = MemoryGame()
            app.MainLoop()
            
        self.playAgainBtn = wx.Button(self.panel, wx.ID_ANY, label="Play Again", pos=(300,90) )
        self.playAgainBtn.Bind(wx.EVT_BUTTON, playAgain)
        self.Show()


#------------------Writing the program------------------------

    def onClick(self, event):
        
        self.clickCount +=1
        newCard = event.GetEventObject()
        #returns the object(usually a window) associate with the event
        img = wx.Image(newCard.GetName(), wx.BITMAP_TYPE_ANY)
        #returns the name of image
        newCard.SetBitmap(wx.Bitmap(img))
        #sets the image to the new image

        if self.clickCount == 1:
            self.card1 = newCard
            self.card1.Unbind(wx.EVT_LEFT_DOWN)

        else:
            self.card2 = newCard
            self.totalTries += 1
            self.statusbar.SetStatusText("Total Tries:" + str(self.totalTries) + "Total Matches:" + str(self.foundMatches))
            if(self.card2.GetName() == self.card1.GetName()):
            #if card two equals card one:
                for findItem in self.deck:
                    if findItem.GetName() == self.card2.GetName():
                        findItem.Unbind(wx.EVT_LEFT_DOWN)
                self.foundMatches +=1
                self.statusbar.SetStatusText("Total Tries:" + str(self.totalTries) + "  Total Matches:" + str(self.foundMatches))
            else:
                print("got to the timer")
                self.timer = wx.Timer(self)
                self.Bind(wx.EVT_TIMER, self.turnCardBack)
                self.timer.Start(500)
            self.clickCount = 0
        
        if self.foundMatches == self.makePairs:
            winner()
            self.statusbar.SetStatusText("Total Tries : " + str(self.totalTries) + "   Total Matches:" + str(self.foundMatches))

    def turnCardBack(self,event):
        print("got to turnCardBack function")
        self.timer.Stop()
        deck = wx.Image("cardBack.jpg", wx.BITMAP_TYPE_ANY)
        self.card2.SetBitmap(wx.Bitmap(deck))
        self.card1.SetBitmap(wx.Bitmap(deck))
        self.card1.Bind(wx.EVT_LEFT_DOWN, self.onClick)
        
        
def winner():
    winner = wx.MessageDialog(None, "You Did it!", style=wx.OK|wx.ICON_INFORMATION)
    winner.ShowModal()
    winner.Destroy()
    return

def GetJpgList(loc):
    jpgs = [f for f in os.listdir(loc) if f [-4:] == ".jpg"]
    return[os.path.join(loc, f) for f in jpgs]

if __name__ == '__main__':
    app = wx.App(False) #adding false tells the app not to redirect errors to a new window
    frame = MemoryGame()
    app.MainLoop()
        

            
        
        

        
