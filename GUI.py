import cv2

def draw_GUI(image1, image2,scores,curr_counter,computer_logic_output,hand_count):
#printing count from hand
    cv2.putText(image1, str(hand_count), (image1.shape[0]//2, image1.shape[1]*3//5), cv2.FONT_HERSHEY_DUPLEX, 4, (255, 255, 0), 25)
    
    #printing score
    cv2.putText(image2, "Score: "+str(scores.score), (image2.shape[0]*1//5, image2.shape[1]*3//5), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 0), 1)
    cv2.putText(image2, "Wickets: "+str(scores.wickets), (image2.shape[0]*1//5, image2.shape[1]*7//10), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 0), 1)
    
    #printing count from computer logic
    cv2.putText(image2, " "+str(computer_logic_output), (image2.shape[0]//2, image2.shape[1]*3//5), cv2.FONT_HERSHEY_SIMPLEX, 4, (255, 255, 0), 25)
    
    #printing out
    if scores.batsman_state=="Out" and not scores.is_game_over():
      cv2.putText(image2, str("Out"), (image2.shape[0]*2//5, image2.shape[1]*2//5), cv2.FONT_HERSHEY_SIMPLEX, 4, (255, 78, 54), 25)
    #printing count
    elif not scores.is_game_over():
      #printing count down  value
      if curr_counter=="Show":
        counter_color=(29, 190, 93)
      else: 
        counter_color=(255, 255, 0)
      cv2.putText(image2, str(curr_counter), (image2.shape[0]//2, image2.shape[1]//5), cv2.FONT_HERSHEY_SIMPLEX, 4, counter_color, 25)

    if scores.is_game_over():
      cv2.putText(image2, str("Game Over"), (image2.shape[0]//9, image2.shape[1]*2//5), cv2.FONT_HERSHEY_SIMPLEX, 3, 	(100,60,20), 20)
    return image1,image2
    