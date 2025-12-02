import pyaudio
import numpy as np
import scipy.signal as signal
import time

# Detects claps from microphone input using audio signal processing

class ClapDetector:
    CHUNK = 1024  # Number of frames per buffer
    FORMAT = pyaudio.paInt16  # 16-bit audio format
    CHANNELS = 1  # Mono channel
    RATE = 44100  # Sample rate in Hz
    THRESHOLD = 1  # Threshold for clap detection
    CLAP_MIN_INTERVAL = 0.2  # Minimum time between claps (s)
    CLAP_LENGTH = 0.05  # Maximum duration of a clap (s)
    CLAPS_RESET_TIME = 1  # Time after which clap count resets (s)
    RECORD_TIME = 5  # Time window for recording claps (s)

    def __init__(self):
        # Initialize audio stream and state variables
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=self.FORMAT,
                                  channels=self.CHANNELS,
                                  rate=self.RATE,
                                  input=True,
                                  frames_per_buffer=self.CHUNK)
        
        self.last_clap_time = time.time()
        self.clap_count = 0
        self.last_detection_time = 0.0
        self.last_clap_count = 0
        self.claps_ready = True
        self.ready_to_read = False

        self.run = True
    
    def __del__(self):
        # Clean up audio stream
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
    
    def detect_claps(self, data):
        """Detects claps in the audio data stream"""
        current_time = time.time()
        
        # Convert data to numpy array
        audio_data = np.frombuffer(data, dtype=np.int16)
        # Normalize audio
        audio_data = audio_data / np.max(np.abs(audio_data))
        # Apply bandpass filter to isolate clap frequencies
        b, a = signal.butter(1, [800 / (self.RATE / 2), 3000 / (self.RATE / 2)], btype='band')
        filtered_data = signal.lfilter(b, a, audio_data)
        # Find peaks in filtered signal
        peaks, _ = signal.find_peaks(filtered_data, height=self.THRESHOLD)
        if len(peaks) > 0:
            # If peak found, check if enough time has passed since last clap
            if (current_time - self.last_clap_time) > self.CLAP_LENGTH:
                self.last_clap_time = current_time
                return 1  # Clap detected
            else:
                return 0  # Too soon after previous clap
        else:
            return 0  # No clap detected


    def start(self):
        """Main loop for clap detection"""
        try:
            while self.run:
                data = self.stream.read(self.CHUNK, exception_on_overflow=False)
                current_time = time.time()

                num_claps = self.detect_claps(data)
                # If clap detected and enough time since last detection
                if num_claps > 0 and (current_time - self.last_detection_time) > self.CLAP_MIN_INTERVAL:
                    self.clap_count += num_claps
                    self.last_detection_time = current_time
                    self.claps_ready = True
                # Reset clap count if enough time has passed
                if (current_time - self.last_detection_time) > self.CLAPS_RESET_TIME:
                    if self.claps_ready:
                        self.claps_ready = False
                        self.ready_to_read = True
                        self.last_clap_count = self.clap_count
                        self.clap_count = 0
                        print('last claps ready', self.last_clap_count)
                # Reset all if record time exceeded
                if (current_time - self.last_detection_time) > self.RECORD_TIME:
                    self.clap_count = 0
                    self.last_clap_count = 0
                    self.ready_to_read = False

                time.sleep(0.01)

        except KeyboardInterrupt:
            print("Detection stopped.")
        finally:
            del self  # Calls destructor and closes stream

    def stop(self):
        """Stop the detection loop"""
        self.run = False

    def get_claps(self):
        """Return last detected clap count"""
        return self.last_clap_count

    def get_status(self):
        """Return if clap count is ready to read"""
        return self.ready_to_read


if __name__ == '__main__':
    # Run clap detection if executed directly
    clap_detector = ClapDetector()
    clap_detector.start()
