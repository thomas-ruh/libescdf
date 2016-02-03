      subroutine lattice_vector_calculation(lattice_parameters, &
                                            lattice_angles,lattice_type)
!                                                                       
!     Transforms lattice parameters and angles into cartesian vectors.
!                                                                       
      use escdf_variables

      implicit none

      double precision,dimension(3) :: lattice_parameters, lattice_angles
      double precision  pi,sqrt3

!!! Adapted up to here
      pi=acos(-1.0d0)                                                   
      sqrt3=sqrt(3.d0)
      lattice_angles(1)=lattice_angles(1)*PI/180.0D0 
      lattice_angles(2)=lattice_angles(2)*PI/180.0D0          
      lattice_angles(3)=lattice_angles(3)*PI/180.0D0        
      lattice_parameters(1)=2.D0*PI/lattice_parameter(1) !!!???         
      lattice_parameters(2)=2.D0*PI/lattice_parameter(2) !!!???          
      lattice_parameters(3)=2.D0*PI/lattice_parameter(3) !!!???      
      if(lattice_type(1:).EQ.'H') goto 10                             
      if(lattice_type(1:).EQ.'S') goto 20                              
      if(lattice_type(1:).EQ.'P') goto 20                             
      if(lattice_type(1:).EQ.'F') goto 30                             
      if(lattice_type(1:).EQ.'B') goto 40                            
      if(lattice_type(1:).EQ.'C') goto 50                             
      if(lattice_type(1:).EQ.'R') goto 60                            
      goto 900
!                                                                       
!.....HEXAGONAL LATTICE                                                 
 10   CONTINUE                                                          
      lattice_vectors(1,1)=2.D0/sqrt3*lattice_parameters(1)
      lattice_vectors(1,2)=1.D0/sqrt3*lattice_parameters(2)     
      lattice_vectors(1,3)=0.0D0                                    
      lattice_vectors(2,1)=0.0D0                                      
      lattice_vectors(2,2)=lattice_parameters(2)      
      lattice_vectors(2,3)=0.0D0                                    
      lattice_vectors(3,1)=0.0D0                                 
      lattice_vectors(3,2)=0.0D0                                     
      lattice_vectors(3,3)=lattice_parameters(3)    
      goto 100                                                          
!                                                                       
!.....RHOMBOHEDRAL CASE                                                    
 60   lattice_vectors(1,1)=1.D0/sqrt(3.D0)*lattice_parameters(1) 
      lattice_vectors(1,2)=1.D0/sqrt(3.D0)*lattice_parameters(1)
      lattice_vectors(1,3)=-2.d0/sqrt(3.d0)*lattice_parameters(1)    
      lattice_vectors(2,1)=-1.0d0*lattice_parameters(2) 
      lattice_vectors(2,2)=1.0d0*lattice_parameters(2) 
      lattice_vectors(2,3)=0.0d0*lattice_parameters(2) 
      lattice_vectors(3,1)=1.0d0*lattice_parameters(3) 
      lattice_vectors(3,2)=1.0d0*lattice_parameters(3) 
      lattice_vectors(3,3)=1.0d0*lattice_parameters(3) 
      goto 100                                                          
!                                                                       
!.....FC LATTICE                                                        
 30   CONTINUE                                                          
      lattice_vectors(1,1)=lattice_parameters(1)   
      lattice_vectors(1,2)=0.0D0                                     
      lattice_vectors(1,3)=0.0D0                                      
      lattice_vectors(2,1)=0.0D0                                     
      lattice_vectors(2,2)=lattice_parameters(2) 
      lattice_vectors(2,3)=0.0D0                                      
      lattice_vectors(3,2)=0.0D0                                       
      lattice_vectors(3,1)=0.0D0                                     
      lattice_vectors(3,3)=lattice_parameters(3)                   
      goto 100                                                          
!                                                                       
!.....BC LATTICE                                                        
 40   CONTINUE                                                          
      lattice_vectors(1,1)=lattice_parameters(1) 
      lattice_vectors(1,2)=0.0D0                                       
      lattice_vectors(1,3)=0.0D0                                      
      lattice_vectors(2,1)=0.0D0                                     
      lattice_vectors(2,2)=lattice_parameters(2) 
      lattice_vectors(2,3)=0.0D0                                       
      lattice_vectors(3,1)=0.0D0                                      
      lattice_vectors(3,2)=0.0D0                                      
      lattice_vectors(3,3)=lattice_parameters(3)       
 
 50   CONTINUE                                                          
      if(LATTIC(2:3).EQ.'XZ') goto 51                          
      if(LATTIC(2:3).EQ.'YZ') goto 52                            
!.....CXY LATTICE                                                          
      lattice_vectors(1,1)=lattice_parameters(1) 
      lattice_vectors(1,2)=0.0D0                                 
      lattice_vectors(1,3)=0.0D0                            
      lattice_vectors(2,1)=0.0D0                                 
      lattice_vectors(2,2)=lattice_parameters(2)
      lattice_vectors(2,3)=0.0D0                                     
      lattice_vectors(3,1)=0.0D0                                      
      lattice_vectors(3,2)=0.0D0                                        
      lattice_vectors(3,3)=lattice_parameters(3)                    
!                                                                       
      goto 100                                                          
!                                                                       
!.....CXZ CASE (CXZ LATTICE BUILD UP)                                     
 51   CONTINUE                                     
!.....CXZ ORTHOROMBIC CASE
      if(ABS(lattice_angles(3)-PI/2.0D0).LT.0.0001) then
         lattice_vectors(1,1)=lattice_parameters(1)            
         lattice_vectors(1,2)=0.0D0                            
         lattice_vectors(1,3)=0.0D0                   
         lattice_vectors(2,1)=0.0D0                      
         lattice_vectors(2,2)=lattice_parameters(2)                
         lattice_vectors(2,3)=0.0D0      
         lattice_vectors(3,1)=0.0D0    
         lattice_vectors(3,2)=0.0D0            
         lattice_vectors(3,3)=lattice_parameters(3)              
         goto 100                                                
      ELSE
!.....CXZ MONOCLINIC CASE
!         write(*,*) 'gamma not equal 90'
         SINAB=SIN(lattice_angles(3))
         COSAB=COS(lattice_angles(3))
!
         lattice_vectors(1,1)= lattice_parameters(1)/SINAB
         lattice_vectors(1,2)= -lattice_parameters(2)*COSAB/SINAB
         lattice_vectors(1,3)= 0.0
         lattice_vectors(2,1)= 0.0
         lattice_vectors(2,2)= lattice_parameters(2)
         lattice_vectors(2,3)= 0.0
         lattice_vectors(3,1)= 0.0
         lattice_vectors(3,2)= 0.0
         lattice_vectors(3,3)= lattice_parameters(3)
!
      ENDif
!                                                                       
!.....CYZ CASE (CYZ LATTICE BUILD UP)                                     
 52   CONTINUE                                     
      lattice_vectors(1,1)=lattice_parameters(1)  
      lattice_vectors(1,2)=0.0D0      
      lattice_vectors(1,3)=0.0D0   
      lattice_vectors(2,1)=0.0D0                     
      lattice_vectors(2,2)=lattice_parameters(2)  
      lattice_vectors(2,3)=0.0D0      
      lattice_vectors(3,1)=0.0D0    
      lattice_vectors(3,2)=0.0D0 
      lattice_vectors(3,3)=lattice_parameters(3)   
      goto 100                                                          
!                                                                       
!
!     TRICLINIC CASE
!                                                                       
20    CONTINUE
      SINBC=SIN(lattice_angles(1))
      COSAB=COS(lattice_angles(3))
      COSAC=COS(lattice_angles(2))
      COSBC=COS(lattice_angles(1))
      WURZEL=sqrt(SINBC**2-COSAC**2-COSAB**2+2*COSBC*COSAC*COSAB)
      lattice_vectors(1,1)= SINBC/WURZEL*lattice_parameters(1)
      lattice_vectors(1,2)= (-COSAB+COSBC*COSAC)/(SINBC*WURZEL)*lattice_parameters(2)
      lattice_vectors(1,3)= (COSBC*COSAB-COSAC)/(SINBC*WURZEL)*lattice_parameters(3)
      lattice_vectors(2,1)= 0.0
      lattice_vectors(2,2)= lattice_parameters(2)/SINBC
      lattice_vectors(2,3)= -lattice_parameters(3)*COSBC/SINBC
      lattice_vectors(3,1)= 0.0
      lattice_vectors(3,2)= 0.0
      lattice_vectors(3,3)= lattice_parameters(3)

100   CONTINUE                                                          
      RETURN
!
!        Error messages
!
900   call OUTERR('LATGEN','wrong lattice.')
      call abort_parallel
      stop 'LATGEN - Error'
!
!        End of 'LATGEN'
!
      end                                                               
