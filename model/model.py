import asyncio
import cv2
import numpy as np
import base64
from typing import List, Dict, Any
from inference_sdk import InferenceHTTPClient
from concurrent.futures import ThreadPoolExecutor

CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="ghdq78iGp8TEMvX2KCar"
)



def process_video(video_path: str, sample_rate: int = 1) -> List[Dict[Any, Any]]:
    """
    Process video frames through inference model.
    
    Args:
        video_path: Path to video file
        sample_rate: Process every Nth frame (default=1)
    
    Returns:
        List of detection results per processed frame
    """
    try:
        # Open video capture
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise ValueError(f"Could not open video: {video_path}")

        results = []
        frame_count = 0
        
        # Create output video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter('output.mp4', fourcc, 30.0, 
                            (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                             int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Process every Nth frame
            if frame_count % sample_rate == 0:
                # Convert frame to base64
                _, buffer = cv2.imencode('.jpg', frame)
                img_base64 = base64.b64encode(buffer).decode('utf-8')
                
                # Run inference
                try:
                    prediction = CLIENT.infer(
                        img_base64,
                        model_id="shoplifting-cuzf8-pl6bp/1"
                    )
                    
                    # Draw predictions
                    for pred in prediction['predictions']:
                        # Extract coordinates
                        x = int(pred['x'])
                        y = int(pred['y'])
                        w = int(pred['width'])
                        h = int(pred['height'])
                        if pred['confidence'] > 0.6:
                            level = 'normal'
                        elif 0.4 <= pred['confidence'] < 0.6:
                            level = 'dangerous'
                        else:
                            level = 'suspicious'
                        # Draw bounding box
                        cv2.rectangle(frame, (x-w//2, y-h//2), (x+w//2, y+h//2), (0, 255, 0), 2)
                        
                        # Add label with confidence

                        label = f"{level}: {pred['confidence']:.2f}"
                        print(pred)
                        cv2.putText(frame, label, (x-w//2, y-h//2-10), 
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    
                    results.append(prediction)
                    
                except Exception as e:
                    print(f"Inference error on frame {frame_count}: {str(e)}")
                    continue
                
                # Write frame to output video
                out.write(frame)
                
                # Display frame (optional)
                cv2.imshow('Frame', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            frame_count += 1

        cap.release()
        out.release()
        cv2.destroyAllWindows()
        return results

    except Exception as e:
        print(f"Error processing video: {str(e)}")
        return []
    
results = process_video("video4.mov", sample_rate=5) 



# def process_webcam(sample_rate=30, scale_factor=0.5):  # Increased sample rate, added scaling
#     try:
#         cap = cv2.VideoCapture(0)
#         if not cap.isOpened():
#             raise Exception("Could not access webcam")
            
#         # Create thread pool for async processing
#         executor = ThreadPoolExecutor(max_workers=1)
#         frame_count = 0
        
#         while True:
#             ret, frame = cap.read()
#             if not ret:
#                 break

#             # Resize frame to improve performance
#             frame = cv2.resize(frame, None, fx=scale_factor, fy=scale_factor)

#             if frame_count % sample_rate == 0:
#                 # Async inference
#                 def process_frame(frame):
#                     _, buffer = cv2.imencode('.jpg', frame)
#                     img_base64 = base64.b64encode(buffer).decode('utf-8')
#                     return CLIENT.infer(img_base64, model_id="shoplifting-cuzf8-pl6bp/1")

#                 future = executor.submit(process_frame, frame)
                
#                 try:
#                     prediction = future.result(timeout=1.0)  # Add timeout
                    
#                     # Draw predictions efficiently
#                     for pred in prediction['predictions']:
#                         x = int(pred['x'] * scale_factor)
#                         y = int(pred['y'] * scale_factor)
#                         w = int(pred['width'] * scale_factor)
#                         h = int(pred['height'] * scale_factor)
                        
#                         # Use faster rectangle drawing
#                         frame[y-h//2:y+h//2, x-w//2:x+w//2] = cv2.addWeighted(
#                             frame[y-h//2:y+h//2, x-w//2:x+w//2], 
#                             0.7, 
#                             np.full_like(frame[y-h//2:y+h//2, x-w//2:x+w//2], [0,255,0]),
#                             0.3, 
#                             0
#                         )
                
#                 except Exception as e:
#                     print(f"Frame processing error: {str(e)}")

#             cv2.imshow('Webcam Feed', frame)
#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                 break

#             frame_count += 1

#         cap.release()
#         cv2.destroyAllWindows()
#         executor.shutdown()

#     except Exception as e:
#         print(f"Error: {str(e)}")

# Run webcam detection
# results = process_webcam(sample_rate=15)