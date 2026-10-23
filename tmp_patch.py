import io, re, sys

path = r'D:\Documents\GitHub\Spopyfly.Web\index.html'
with io.open(path, 'r', encoding='utf-8', newline='') as f:
    src = f.read()

start_marker = "      function extractYTVideoId(str) {"
end_marker = "      });\n\n"
i = src.index(start_marker)
j = src.index(end_marker, i) + len(end_marker)

new = '''      function extractYTVideoId(str) {
        const patterns = [
          /(?:youtube\\.com\\/watch\\?[^\\s]*v=|youtu\\.be\\/|youtube\\.com\\/embed\\/|youtube\\.com\\/shorts\\/|youtube\\.com\\/live\\/)([a-zA-Z0-9_-]{11})/,
          /^([a-zA-Z0-9_-]{11})$/ // Raw video ID
        ];
        for (const p of patterns) {
          const m = str.match(p);
          if (m) return m[1];
        }
        return null;
      }

      // Add and play any video by its ID. Title and cover come from YouTube
      // oEmbed first, then a mirror, then a plain thumbnail. No API key needed.
      async function addFromYouTubeId(vid) {
        if (!vid) return;
        const input = document.getElementById('searchInput');
        if (input) input.value = '';
        renderSearch('');
        showToast('Fetching YouTube track\\u2026', '');
        let s = null;
        try {
          const r = await fetch('https://www.youtube.com/oembed?url=' + encodeURIComponent('https://www.youtube.com/watch?v=' + vid) + '&format=json', { cache: 'no-store' });
          if (r.ok) {
            const data = await r.json();
            s = { title: ytClean(data.title) || 'YouTube Track', artist: ytClean(data.author_name) || 'YouTube', cover: data.thumbnail_url || ytThumb(vid), vid };
          }
        } catch (e) { /* try the mirrors next */ }
        if (!s) {
          for (const m of YT_MIRRORS) {
            if (m.kind !== 'piped') continue;
            try {
              const d = await fetchJSON(m.host + '/streams/' + encodeURIComponent(vid), 6000);
              if (d && d.title) { s = { title: ytClean(d.title), artist: ytClean(d.uploader) || 'YouTube', cover: ytThumb(vid), vid }; break }
            } catch (e) { /* next mirror */ }
          }
        }
        if (!s) s = { title: 'YouTube Track (' + vid + ')', artist: 'YouTube', cover: ytThumb(vid), vid };
        addAndPlay(s);
        showToast('Added: ' + s.title.slice(0, 34), '');
      }

      // Paste a YouTube link or video ID into the search box: add and play it.
      const origSearchInput = document.getElementById('searchInput');
      origSearchInput.addEventListener('paste', (e) => {
        const pasted = ((e.clipboardData || window.clipboardData).getData('text') || '').trim();
        const vid = extractYTVideoId(pasted);
        if (!vid) return;
        e.preventDefault();
        clearTimeout(searchTimer);
        addFromYouTubeId(vid);
      });

'''

src = src[:i] + new + src[j:]
with io.open(path, 'w', encoding='utf-8', newline='') as f:
    f.write(src)
print('ok')
