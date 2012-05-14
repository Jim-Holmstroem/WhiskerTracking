from wmedia import wanimation

class ParticleAnimator(wanimation):
    def __init__(self, track, resampled_particles, preresampled_particles, track_color=(0,255,0), resampled_particles_color=(255,0,0), preresampled_particles_color=(0,0,255), alpha=0.1, highest_weight_particles=None, highest_weight_particle_color=(255,255,0), **other_kwargs):
        self.resampled_particles = resampled_particles
        self.track = track
        self.preresampled_particles = preresampled_particles
        self.highest_weight_particles = highest_weight_particles
        self.alpha = alpha
        
        self.track_color = track_color
        self.resampled_particles_color = resampled_particles_color
        self.preresampled_particles_color = preresampled_particles_color
        self.highest_weight_particle_color = highest_weight_particle_color
        
        self.data_renderer = self.render
    
    def __len__(self):
        if self.resampled_particles != None:
            return len(self.resampled_particles)
        elif self.track != None:
            return len(self.track)
        return 0
    
    def render(self, context, i):
        if self.preresampled_particles != None:
            for row in self.preresampled_particles[i]:
                self.renderer.render(context, row, self.preresampled_particles_color, filled=False, alpha=0.1)
        
        if self.resampled_particles != None:
            for row in self.resampled_particles[i]:
                self.renderer.render(context, row, self.resampled_particles_color, filled=False, alpha=0.1)
        
        if self.track != None:
            self.renderer.render(context, self.track[i], self.track_color, filled=False, alpha=1)

        if self.highest_weight_particles != None:
            self.renderer.render(context, self.highest_weight_particles[i], self.highest_weight_particle_color, filled=True, alpha=0.5)
