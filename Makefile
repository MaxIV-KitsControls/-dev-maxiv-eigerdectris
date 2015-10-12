#=============================================================================
#
# file :        Makefile
#
# description : Include for the EigerDectris class.
#
# project :     Makefile to generate a Tango server
#
# $Author:  $
#
# $Revision: $
#
#
# copyleft :    European Synchrotron Radiation Facility
#               BP 220, Grenoble 38043
#               FRANCE
#
#=============================================================================
#  		This file is generated by POGO
#	(Program Obviously used to Generate tango Object)
#
#         (c) - Software Engineering Group - ESRF
#=============================================================================
#
MAKE_ENV = $(TANGO_DIR)/Libraries/cppserver/common
CLASS      = EigerDectris
MAJOR_VERS = 1
MINOR_VERS = 0
RELEASE    = Release_$(MAJOR_VERS)_$(MINOR_VERS)

#-----------------------------------------
#	 Install binary file
#-----------------------------------------
all:
	@echo "Nothing to do"

ifdef using_trunk
	FILEWRITER_DIR = $(TANGO_DIR)/DeviceClasses/Acquisition/2D/EigerFilewriter/trunk
	MONITOR_DIR = $(TANGO_DIR)/DeviceClasses/Acquisition/2D/EigerMonitor/trunk
else
	FILEWRITER_DIR = $(TANGO_DIR)/DeviceClasses/Acquisition/2D/EigerFilewriter/tags -type d -regex '.*Release_[0-9]*_[0-9]*' | sort -t '_' -k2 -k3 -nr | head -1)
	MONITOR_DIR = $(TANGO_DIR)/DeviceClasses/Acquisition/2D/EigerMonitor/tags -type d -regex '.*Release_[0-9]*_[0-9]*' | sort -t '_' -k2 -k3 -nr | head -1)	

install:
	cp $(CLASS).py  $(DESTDIR)
	cp $(CLASS)  $(DESTDIR)
	cp -r dectris_eiger $(DESTDIR)
	cp $(FILEWRITER_DIR)/EigerFilewriter.py $(DESTDIR)
	cp $(MONITOR_DIR)/EigerMonitor.py $(DESTDIR)
	chmod 755 $(DESTDIR)/$(CLASS)

clean:
	@echo "Nothing to do"

include $(MAKE_ENV)/common_target.opt

#----------------------------------------------------
#	Tag the SVN module corresponding to this class
#----------------------------------------------------


tag:
ifeq ($(shell ls -d ../tags/$(RELEASE) 2>/dev/null ), ../tags/$(RELEASE))
	@echo $(RELEASE) exists, specify new version numbers
else
	svn copy ../trunk ../tags/$(RELEASE)
	svn commit ../tags/$(RELEASE) \
	-m "Tagging the $(RELEASE) of the $(CLASS) project."
endif
