import os
import numpy as np
import scipy.stats as ss

from psychopy import prefs
prefs.hardware['audioLib'] = ['PTB']
from psychopy import sound

from exptools2.core import Session, PylinkEyetrackerSession
from psychopy.visual import MovieStim3
from trial import SomaVisualTrial, InstructionTrial, DummyWaiterTrial, OutroTrial
from stimuli import FixationLines


class SomaVisualSession(PylinkEyetrackerSession):
    def __init__(self, output_str, output_dir, settings_file, eyetracker_on=True, task='VM'):
        """ Initializes StroopSession object. 
      
        Parameters
        ----------
        output_str : str
            Basename for all output-files (like logs), e.g., "sub-01_task-stroop_run-1"
        output_dir : str
            Path to desired output-directory (default: None, which results in $pwd/logs)
        settings_file : str
            Path to yaml-file with settings (default: None, which results in the package's
            default settings file (in data/default_settings.yml)
        """
        super().__init__(output_str, output_dir=output_dir, settings_file=settings_file, eyetracker_on=eyetracker_on)  # initialize parent class!
        self.n_trials = self.settings['design'].get('n_trials')  
        self.task = task
        print(f'running expt using task {task}')

        # fugly hack to avoid wait at startup
        self.win._monitorFrameRate = 60.0

        self.movies = [
            'eyebrows',
            'eyes',
            'mouth',
            'tongue',
            'lhand_fing1', 
            'lhand_fing2', 
            'lhand_fing3', 
            'lhand_fing4', 
            'lhand_fing5', 
            'lleg', 
            'eyebrows',
            'eyes',
            'mouth',
            'tongue',
            'bhand_fing1', 
            'bhand_fing2', 
            'bhand_fing3', 
            'bhand_fing4', 
            'bhand_fing5', 
            'bleg', 
            'tongue',
            'mouth',
            'eyes',
            'eyebrows',
            'rhand_fing1', 
            'rhand_fing2', 
            'rhand_fing3', 
            'rhand_fing4', 
            'rhand_fing5', 
            'rleg',
            'eyebrows',
            'eyes',
            'mouth',
            'tongue',
            'lhand_fing5', 
            'lhand_fing4', 
            'lhand_fing3', 
            'lhand_fing2', 
            'lhand_fing1', 
            'lleg', 
            'eyebrows',
            'eyes',
            'mouth',
            'tongue',
            'bhand_fing5', 
            'bhand_fing4', 
            'bhand_fing3', 
            'bhand_fing2', 
            'bhand_fing1', 
            'bleg', 
            'tongue',
            'mouth',
            'eyes',
            'eyebrows',
            'rhand_fing5', 
            'rhand_fing4', 
            'rhand_fing3', 
            'rhand_fing2', 
            'rhand_fing1', 
            'rleg'
        ]
        self.unique_movies = list(np.unique(self.movies))
        self.unique_movie_files = [os.path.join(os.path.abspath(os.getcwd()), 'stimuli', 'movs',  m+".mp4") for m in self.unique_movies]
        self.unique_sound_files = [os.path.join(os.path.abspath(os.getcwd()), 'stimuli', 'sounds',  m+".wav") for m in self.unique_movies]
        # self.unique_movie_files = [os.path.join(os.path.abspath(os.getcwd()), 'stimuli', 'movs',  'op', m+"_small.avi") for m in self.unique_movies]

        self.unique_movie_stims = [MovieStim3(self.win, filename=imf, loop=True, noAudio=True) for imf in self.unique_movie_files]
        self.unique_sound_stims = [sound.Sound(value=sf) for sf in self.unique_sound_files]

        self.movie_stims = [self.unique_movie_stims[self.unique_movies.index(s)] for s in self.movies]
        self.sound_stims = [self.unique_sound_stims[self.unique_movies.index(s)] for s in self.movies]

        # movie_files = [os.path.join(os.path.abspath(os.getcwd()), 'stimuli', 'movs',  '%s'%m) for m in self.movies]
        # sound_files = [os.path.join(os.path.abspath(os.getcwd()), 'stimuli', 'sounds',  '%s'%m) for m in self.movies]

        print(f'running expt with movies {self.movie_stims}')

        # self.movie_stims = [MovieStim3(self.win, filename=imf, size=self.win.size) for imf in movie_files]
        # self.sound_stims = [sound.Sound(value=sf.replace('.mp4', '.mp3')) for sf in sound_files]
        # print(f'loaded movie files')

        self.fix_stim = FixationLines(self.win, circle_radius=self.win.size[1], color=(-1,-1,-1))

        self.create_trials()

    def create_trials(self):
        """ Creates trials (ideally before running your session!) """
        
        if self.task == 'VM':
            instruct_text = 'fixate at the center, move in unison with movies'
        elif self.task == 'VO':
            instruct_text = 'fixate at the center, DO NOT move'
        elif self.task == 'AM':
            instruct_text = 'close your eyes when scanner starts, move in unison with instruction'
        print(instruct_text)

        instruction_trial = InstructionTrial(session=self, 
                                            trial_nr=0, 
                                            phase_durations=[np.inf],
                                            txt=instruct_text,
                                            keys=['space'])

        dummy_trial = DummyWaiterTrial(session=self, 
                                            trial_nr=1, 
                                            phase_durations=[np.inf, self.settings['design'].get('start_duration')],
                                            txt='Waiting for experiment to start')

        outro_trial = OutroTrial(session=self, 
                                            trial_nr=len(self.movies)+2, 
                                            phase_durations=[self.settings['design'].get('end_duration')],
                                            txt='')



        self.trials = [instruction_trial, dummy_trial]
        for i in range(len(self.movies)):
            self.trials.append(SomaVisualTrial(
                session=self, 
                trial_nr=2+i, 
                phase_durations=[0.001, self.settings['design'].get('stim_duration')], 
                phase_names=['iti', 'stim'],
                parameters={'stimulus': self.movies[i], 'which_movie': i}, 
                timing='seconds',
                verbose=True))
            print(f'created trial {i}')

        self.trials.append(outro_trial)

    def create_trial(self):
        pass

    def run(self):
        """ Runs experiment. """   
        # self.create_trials()  # create them *before* running!

        if self.eyetracker_on:
            self.calibrate_eyetracker()

        self.start_experiment()

        if self.eyetracker_on:
            self.start_recording_eyetracker()
        for trial in self.trials:
            trial.run()

        self.close()
    