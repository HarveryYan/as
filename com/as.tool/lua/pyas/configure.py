import os
import sys
import glob
import sipconfig 

def sip_makefile(sipfile,output):
    module = sipfile[:-4]
    
    # The name of the SIP build file generated by SIP and used by the build
    # system.
    build_file = "%s.sbf"%(module)
    
    # Get the SIP configuration information.
    config = sipconfig.Configuration()
    
    # compiler sip
    os.system(" ".join([config.sip_bin, "-c", output, sipfile]))
    
    # Run SIP to generate the code.
    os.system(" ".join([config.sip_bin, "-c", output, "-b", build_file, "%s.sip"%(module)]))
    
    # Create the Makefile.
    makefile = sipconfig.SIPModuleMakefile(config, build_file)
    
    # Add the library we are wrapping.  The name doesn't include any platform
    # specific prefixes or extensions (e.g. the "lib" prefix on UNIX, or the
    # ".dll" extension on Windows).
    makefile.extra_libs = [module,'aws','pthread','m']
    makefile.extra_lib_dirs = [output]
    makefile.extra_defines  = []
    makefile.extra_cflags = ['--std=gnu99','-I$(LUA)/pyas']
    if(os.name=='nt'):
       makefile.extra_libs.append('PCANBasic')
       makefile.extra_libs.append('pyas')
       makefile.extra_libs.append('wsock32')
    # Generate the Makefile itself.
    makefile.generate()
    
if(__name__ == '__main__'):
    if(len(sys.argv)==3):
        sip_makefile(sys.argv[1], sys.argv[2])  
    else:
        print("Usage:\n\t %s python_sip_script output\n\texample: %s ./pycan.sip ./pycan\n"%(sys.argv[0],sys.argv[0])) 
        
