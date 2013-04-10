
"""
 Sikuli Regions

It is worth spending some time looking at how Sikuli Regions work. Unit testing
in only the simplest of cases involves finding an image singleton on the
screen. Unit Testing often involves selecting many similar objects and cycling
through various combinations. Understanding Regions allows the script designer
to focus the Sikuli scope to a subsection of the display, including or
excluding graphical objects at will. The PNG image below is based on the Sikuli
Region documentation. It contains a bit more information, but more importatntly
is used with the Sikuli script below to provide an interactive way of exploring
the Region methods.

Diagram of Extending a Sikuli Region


The white area is Reference Region. Above, Below, Left and Right are shown in different colours and DO NOT contain the reference region. Nearby is the only function that increases the size of the Reference Region.  The resulting regions from the PNG file that are created using the extension functions are shown below.   

The order of operation of the extension functions is very important as can be seen in the example below. nearby().above() increases all the Reference Region's edges by the default 50 pixels, then extends from this new box to the top of the screen.  above().nearby() selects the area to the top of the Reference region to the top of the screen, then increases this area by 50 pixels which re-includes some of the Reference Region.


It is possible to include the Reference Region and a new region. A region is set through x,y,width and height parameters. In the example below, the .above() region is combined with the Reference Region.

"""

ReferenceRegion = find("PriimaryRegion.PNG")
#Start at the top of the screen
ReferenceRegion .setY( 0 )
#The height is now the combination of the ReferenceRegion and the height above
ReferenceRegion.setH(ReferenceRegion.H + ReferenceRegion.above().H)
#The X and W dimensions are unchanged 


"""The Sikuli script below uses Greenshot to copy and paste different areas to
help visualize the different Sikuli areas.  Copy and paste into a sikuli
project and add the two images that follow the script."""


"""Demonstrates sikuli regions.  Copies different regions of a PNG file to
Greenshot's clipboard.  CaptureRegion and CloseCapture are really important
general purpose debugging tools.  Keep these close at hand.
   
   Requires GreenShot to create the screen captures.
   http://sourceforge.net/projects/greenshot/

   Open Greenshot and Firefox on the same screen.  If Greenshot is on a
   different screen, the close will not work correctly.  Do not change
   applications between popup windows or Greenshot may not close (another
   program may close instead)
   """

#openApp("C:\\Program Files\\Mozilla Firefox\\firefox.exe file:///M:\\SikuliExamples\Regions.sikuli\\sikuliRegions.PNG")
openApp("C:\\Program Files\\Mozilla Firefox\\firefox.exe 
http://2.bp.blogspot.com/-YUq5PCEwIe0/T2PEKdr9K4I/AAAAAAAAABc/YeAxXapQNVQ/s1600/sikuliRegions.PNG")

#-------------------------------------------------------------------------------------------------------------------
def CaptureRegion( R ):
    """Capture the Region using Greenshot.  If the processor speed is too slow
    the dragDrop can occur before the capture is complete.  In such an event,
    extend the first wait state.  Greenshot must be launched before exiting the
    function (otherwise there may be a race condition).  Extend the second wait
    state if Greenshot does not seem to launch at the correct time in your
    script

       Keyword arguments:
           R   Region to capture
    """

    # Capture the entire screen with Greenshot using the Print Screen button.    
    type(Key.PRINTSCREEN)
    wait(2)
    # Highlight the area of interest.  The drop will launch Greenshot
    dragDrop(R.getBottomLeft(),R.getTopRight() )
    wait(1)

#-------------------------------------------------------------------------------------------------------------------
def CloseCapture():
    """ Close Greenshot disposing of the image.  Greenshot must be the
    application in focus, if not a different Windows app will receive the close
    command.  The App("Greenshot").focus() command does not work."""

    switchApp("Greenshot image editor - sikuliRegions.PNG (PNG Image, ") 
    wait(1)
    type('f', KeyModifier.ALT)
    type(Key.UP)
    type(Key.ENTER)

    # If the screenshot contains the mouse, Greenshot will prompt the user.
    # Dismiss the save.

    wait(1) 
    if exists( Pattern("Dialog_GreenshotSave.png").targetOffset(-2,36),1):
        type('N')


#===================================================================================================================
PrimaryRegion = find("PriimaryRegion.PNG")

CaptureRegion(PrimaryRegion)
popup("This is the PrimaryRegion")
CloseCapture()

CaptureRegion( PrimaryRegion.above() )
popup(".above()\nDoes not include PrimaryRegion")
CloseCapture()
CaptureRegion( PrimaryRegion.below() )
popup(".below()\n Extends to the bottom of the Screen")
CloseCapture()
CaptureRegion( PrimaryRegion.left() )
popup(".left()")
CloseCapture()
CaptureRegion( PrimaryRegion.right() )
popup(".right()\nBy default does not extend to the second screen.")
CloseCapture()

CaptureRegion( PrimaryRegion.above().right() )
popup("above().right()\nDoes not include either PrimaryRegion.above() or PrimaryRegion.right()")
CloseCapture()
CaptureRegion( PrimaryRegion.below().right() )
popup("below().right()")
CloseCapture()
CaptureRegion( PrimaryRegion.above().left() )
popup("above().left()")
CloseCapture()
CaptureRegion( PrimaryRegion.below().left() )
popup("below().left()")
CloseCapture()

CaptureRegion(PrimaryRegion.nearby())
popup(".nearby()\nNearby increases each region edge by default 50 pixels")
CloseCapture()
CaptureRegion(PrimaryRegion.nearby(5))
popup(".nearby(5)\n The default pixel size can be overridden")
CloseCapture()
CaptureRegion(PrimaryRegion.nearby(100))
popup(".nearby(100)");
CloseCapture()


CaptureRegion(PrimaryRegion.nearby().above())
popup(".nearby().above()\nOrder of operation is important.")
CloseCapture()
CaptureRegion(PrimaryRegion.above().nearby())
popup("above().nearby()")
CloseCapture()

# Create a list of .PNG files that are a part of the project that are not explicitly defined in the Sikuli script.
# Without this tuple, the Sikuli IDE will automatically delete the images.
#https://answers.launchpad.net/sikuli/+question/151185
myImages = ("sikuliRegions.PNG","sikuliRegionsWithLogos.PNG");


