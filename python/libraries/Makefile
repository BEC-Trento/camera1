###### EDIT ##################### 
#Directory with ui and resource files
RESOURCE_DIR = .

#Destination directory for the compiled files
COMPILED_DIR = .

#Qt resource files to compile
RESOURCES = resources.qrc 
 
#pyuic4 and pyrcc4 binaries
#PYUIC = pyuic4
PYRCC = pyrcc4
 
#################################
# DO NOT EDIT FOLLOWING
 
COMPILED_RESOURCES = $(RESOURCES:%.qrc=$(COMPILED_DIR)/%_rc.py)
 
resources:  $(COMPILED_RESOURCES) 
 
$(COMPILED_DIR)/%_rc.py : $(RESOURCE_DIR)/%.qrc
	$(PYRCC) $< -py3 -o $@
 
clean : 
	rm $(COMPILED_RESOURCES) $(COMPILED_RESOURCES:.py=.pyc)
