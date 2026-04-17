import sys

replacements = {
    "'J3e3mC0G3Gk'": "'5Uuq9dTBXII'",
    "'jwnsMH1OSCA'": "'Wf83i2p846s'", 
    "'OcFU6BphLj4'": "'Htcj5HTjnLI'",
    "'YwPFNmk82Z4'": "'zRCjgZIua_A'",
    "'nJl5oMnGe7A'": "'fg_65zkb0cY'",
    "'Ntp1KgBMqAE'": "'vvRmMCavmCA'",
    "'yOEJvZNREYk'": "'TPh74LLdXuw'",
    "'cUgJwq6IGPI'": "'WBsXA3Tq2A0'",
    "'1fT2F_D08vM'": "'nLZtEWyLpF0'",
    "'c5s7t302G-8'": "'mAh-kccZ77Y'",
    "'K48VbO1_U1c'": "'oBZ1eeOpF94'",
    "'t-dM1t_G1jM'": "'5DSBxFZaycA'",
    "'rN9Lw49x6gQ'": "'1dBEGtAPogQ'",
    "'P5Wj2tKx_4w'": "'N2Ntljr_m_0'",
    "'uH-KjJ0Wf-o'": "'VSxTJylaIok'",
    "'WP61j0TXPAM'": "'uNvrG16HIVY'",
    "'f0s6oG2J-nI'": "'5HZ9qeFjhYk'",
    "'DGpzBOSiyxY'": "'rKGOC6OSivg'",
    "'aG3l7g7m8Wk'": "'PWla_-1E6iI'",
    "'QfnBpb6lRoA'": "'jchE-1C7DXE'",
    "'0_X0J9y34c0'": "'rTgE55kRF0g'",
    "'37k-7Z5rL6A'": "'WW7EFEJUUlE'",
    "'hR-vO1O0L4A'": "'9GOBbUTZ9IA'",
    "'gqmommWDoGY'": "'Z82-WwY828k'",
    "'Z82-WwY828k'": "'gqmommWDoGY'",
    "'j5hcNbbpWQk'": "'aJakSXHZROo'",
    "'Bm3xGPFh4FU'": "'Svm0vY91oN0'",
    "'w2c7Z543uYk'": "'0Yq2LEhHJO4'",
    "'20hR5c1R2_8'": "'Ftma0A_Blzc'",
    "'y0Vb_mZq71w'": "'74450Da30R8'",
    "'kYJ5o-v3vT4'": "'BkPd_MKyp_s'",
    "document.getElementById('btnPlayPause').onclick = playPause;": "document.getElementById('btnPlay').onclick = togglePlay;",
    "document.getElementById('btnNext').onclick = nextTrack;": "document.getElementById('btnNext').onclick = next;",
    "document.getElementById('btnPrev').onclick = prevTrack;": "document.getElementById('btnPrev').onclick = prev;",
    "state.isShuffle = !state.isShuffle;": "S.shuffle = !S.shuffle;",
    "state.isRepeat = !state.isRepeat;": "S.repeat = !S.repeat;",
    "document.getElementById('volumeSlider').oninput = (e) => setVolume(parseInt(e.target.value, 10));": "document.getElementById('volSlider').oninput = (e) => setVol(parseInt(e.target.value, 10));",
    "document.getElementById('playerLike').onclick": "document.getElementById('null_element') /*.onclick",
    "document.getElementById('nowPlayingOverlay').classList": "document.getElementById('npOverlay').classList",
    "document.getElementById('btnFullscreen').onclick": "document.getElementById('btnExpand').onclick",
    "document.getElementById('overlayClose').onclick": "document.getElementById('npClose').onclick",
    "state.currentTrackIndex !== -1": "S.idx !== -1",
    "document.getElementById('btnVideo').onclick = toggleVideoOverlay;": "// removed unused btnVideo initialization",
    "state.isPlaying": "S.playing"
}

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re

# To fix the playerLike block, we can comment it out entirely since it throws errors.
old_like_block = '''      /* Like button */
      document.getElementById('playerLike').onclick = function () {
        state.isLiked = !state.isLiked;
        this.classList.toggle('liked', state.isLiked);
        const icon = this.querySelector('i');
        if (icon) icon.setAttribute('data-lucide', state.isLiked ? 'heart' : 'heart');
        if (state.isLiked) this.querySelector('i').style.color = 'var(--accent)';
        else this.querySelector('i').style.color = '';
        safeLucide();
      };'''

new_like_block = '''      /* Like button logic removed as element no longer exists */'''

content = content.replace(old_like_block, new_like_block)

old_player_controls = '''      /* Player controls */
      document.getElementById('btnPlayPause').onclick = playPause;
      document.getElementById('btnNext').onclick = nextTrack;
      document.getElementById('btnPrev').onclick = prevTrack;
      document.getElementById('btnShuffle').onclick = function () { state.isShuffle = !state.isShuffle; this.classList.toggle('active'); };
      document.getElementById('btnRepeat').onclick = function () { state.isRepeat = !state.isRepeat; this.classList.toggle('active'); };
      document.getElementById('seekBar').oninput = (e) => seekTo(parseFloat(e.target.value));
      document.getElementById('volumeSlider').oninput = (e) => setVolume(parseInt(e.target.value, 10));
      document.getElementById('btnMute').onclick = toggleMute;'''

new_player_controls = '''      /* Player controls */
      document.getElementById('btnPlay').onclick = togglePlay;
      document.getElementById('btnNext').onclick = next;
      document.getElementById('btnPrev').onclick = prev;
      document.getElementById('btnShuffle').onclick = function () { S.shuffle = !S.shuffle; this.classList.toggle('active'); };
      document.getElementById('btnRepeat').onclick = function () { S.repeat = !S.repeat; this.classList.toggle('active'); };
      document.getElementById('seekBar').oninput = (e) => seekTo(parseFloat(e.target.value));
      document.getElementById('volSlider').oninput = (e) => setVol(parseInt(e.target.value, 10));
      document.getElementById('btnMute').onclick = toggleMute;'''

content = content.replace(old_player_controls, new_player_controls)

old_now_playing = '''      /* Now Playing overlay */
      document.getElementById('playerCover').closest('.player-cover-wrap').onclick = () => {
        if (state.currentTrackIndex !== -1) document.getElementById('nowPlayingOverlay').classList.add('open');
      };
      document.getElementById('overlayClose').onclick = () => document.getElementById('nowPlayingOverlay').classList.remove('open');
      document.getElementById('btnFullscreen').onclick = () => {
        if (state.currentTrackIndex !== -1) document.getElementById('nowPlayingOverlay').classList.toggle('open');
      };
      document.getElementById('overlayPlayPause').onclick = playPause;
      document.getElementById('overlayNext').onclick = nextTrack;
      document.getElementById('overlayPrev').onclick = prevTrack;
      document.getElementById('overlaySeekBar').oninput = (e) => seekTo(parseFloat(e.target.value));'''

new_now_playing = '''      /* Now Playing overlay */
      if (document.getElementById('playerCover')) {
        document.getElementById('playerCover').closest('.player-cover-wrap').onclick = () => {
          if (S.idx !== -1) document.getElementById('npOverlay').classList.add('open');
        };
      }
      if (document.getElementById('npClose')) {
        document.getElementById('npClose').onclick = () => document.getElementById('npOverlay').classList.remove('open');
      }
      if (document.getElementById('btnExpand')) {
        document.getElementById('btnExpand').onclick = () => {
          if (S.idx !== -1) document.getElementById('npOverlay').classList.toggle('open');
        };
      }
      if (document.getElementById('npPlay')) document.getElementById('npPlay').onclick = togglePlay;
      if (document.getElementById('npNext')) document.getElementById('npNext').onclick = next;
      if (document.getElementById('npPrev')) document.getElementById('npPrev').onclick = prev;
      if (document.getElementById('npSeekBar')) document.getElementById('npSeekBar').oninput = (e) => seekTo(parseFloat(e.target.value));'''

content = content.replace(old_now_playing, new_now_playing)

old_video_overlay = '''      /* Video overlay */
      document.getElementById('btnVideo').onclick = toggleVideoOverlay;
      document.getElementById('videoClose').onclick = closeVideoOverlay;
      document.getElementById('videoTheater').onclick = toggleTheaterMode;
      document.getElementById('videoMinimize').onclick = minimizeVideo;
      document.getElementById('videoExpand').onclick = expandVideo;
      document.getElementById('videoMiniExpand').onclick = expandVideo;
      document.getElementById('videoMiniClose').onclick = closeVideoOverlay;'''

new_video_overlay = '''      /* Video overlay */
      if(document.getElementById('btnVideo')) document.getElementById('btnVideo').onclick = toggleVideoOverlay;
      if(document.getElementById('videoClose')) document.getElementById('videoClose').onclick = closeVideoOverlay;
      if(document.getElementById('videoTheater')) document.getElementById('videoTheater').onclick = toggleTheaterMode;
      if(document.getElementById('videoMinimize')) document.getElementById('videoMinimize').onclick = minimizeVideo;
      if(document.getElementById('videoExpand')) document.getElementById('videoExpand').onclick = expandVideo;
      if(document.getElementById('videoMiniExpand')) document.getElementById('videoMiniExpand').onclick = expandVideo;
      if(document.getElementById('videoMiniClose')) document.getElementById('videoMiniClose').onclick = closeVideoOverlay;'''

content = content.replace(old_video_overlay, new_video_overlay)

for old, new in replacements.items():
    content = content.replace(old, new)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Replaced successfully!")
