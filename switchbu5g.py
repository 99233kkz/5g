
def switchbu(x,y):
    match x:
        case 'VBPc5':
            if y==64 or y==8:
                return 3
            elif y==4 or y==2:
                return 6
            else:
                return 0
        case 'VBPd0b':
            if y==64 or y==8 or y==32:
                return 3
            elif y==4 or y==2:
                return 6
            else:
                return 0
        case 'VBPd0c':
            if y==8 or y==32:
                return 3
            elif y==4 or y==2:
                return 6
            else:
                return 0
        case 'VBPd0d':
            if y==4:
                return 3
            else:
                return 0
        case 'VBPd0f':
            if y==4:
                return 6
            else:
                return 0    
        case 'VBPd2f':
            if y==4:
                return 12
            else:
                return 0
        case 'VBPd3':
            if y==8 or y==4 or y==2:
                return 6
            else:
                return 0    
        case 'VBPd4':
            if y==8:
                return 3
            elif y==4 or y==2:
                return 6
            else:
                return 0
        case 'VBPd5b':
            if y==64 or y==32:
                return 6
            else:
                return 0    
        case 'VBPd5c':
            if y==32:
                return 6
            else:
                return 0    
        case 'VBPe0a':
            if y==8:
                return 3
            elif y==4 or y==2:
                return 6
            else:
                return 0    
        case 'VBPe0b':
            if y==64 or y==32 or y==8:
                return 3            
            elif y==4 or y==2:
                return 6
            else:
                return 0    
        case 'VBPe0d':
            if y==4:                
                return 3
            else:
                return 0        
        case 'VBPe0f':
            if y==4:
                return 6
            else:
                return 0    
        case 'VBPe5b':
            if y==64 or y==32:
                return 6
            else:
                return 0        
        case 'VBPe5c':
            if y==32:
                return 9
            else:
                return 0        
        case 'VBPe5a':
            if y==8:
                return 6
            elif y==4:
                return 9
            elif y==2:
                return 12
            else:
                return 0        
        case 'VBPe0c':
            if y==8 or y==32:
                return 3
            elif y==4 or y==2:
                return 6
            else:
                return 0        

