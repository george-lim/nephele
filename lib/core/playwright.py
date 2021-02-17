import brotli
import io
import os
import pathlib
import playwright
import tarfile

_AWS_LIB_PATH = pathlib.Path('/tmp/aws/lib')
_CHROMIUM_BINARY_PATH = pathlib.Path('/tmp/chromium')
_CHROMIUM_PACKAGE_PATH = pathlib.Path('/opt/chromium')

_NAVIGATION_TIMEOUT_MS = 10000

_CHROMIUM_ARGS = [
  '--autoplay-policy=user-gesture-required',
  '--disable-background-networking',
  '--disable-background-timer-throttling',
  '--disable-backgrounding-occluded-windows',
  '--disable-breakpad',
  '--disable-client-side-phishing-detection',
  '--disable-component-update',
  '--disable-default-apps',
  '--disable-dev-shm-usage',
  '--disable-domain-reliability',
  '--disable-extensions',
  '--disable-features=AudioServiceOutOfProcess',
  '--disable-hang-monitor',
  '--disable-ipc-flooding-protection',
  '--disable-notifications',
  '--disable-offer-store-unmasked-wallet-cards',
  '--disable-popup-blocking',
  '--disable-print-preview',
  '--disable-prompt-on-repost',
  '--disable-renderer-backgrounding',
  '--disable-setuid-sandbox',
  '--disable-speech-api',
  '--disable-sync',
  '--disk-cache-size=33554432',
  '--hide-scrollbars',
  '--ignore-gpu-blacklist',
  '--metrics-recording-only',
  '--mute-audio',
  '--no-default-browser-check',
  '--no-first-run',
  '--no-pings',
  '--no-sandbox',
  '--no-zygote',
  '--password-store=basic',
  '--use-gl=swiftshader',
  '--use-mock-keychain',
  '--single-process'
]

class Playwright:
  def __init__(self, user_id):
    self.screenshot_path = pathlib.Path(f'/tmp/{user_id}/playwright_screenshot.png')

  def _extract_chromium(self):
    if _CHROMIUM_BINARY_PATH.exists():
      return

    for brotli_archive in _CHROMIUM_PACKAGE_PATH.iterdir():
      if brotli_archive.suffix != '.br':
        continue

      extract_path = pathlib.Path(f'/tmp/{brotli_archive.stem}')
      decompressed_bytes = brotli.decompress(brotli_archive.read_bytes())

      if extract_path.suffix == '.tar':
        with tarfile.open(fileobj=io.BytesIO(decompressed_bytes)) as tar:
          tar.extractall(extract_path.with_suffix(''))
      else:
        extract_path.write_bytes(decompressed_bytes)
        extract_path.chmod(0o755)

  def _set_environment_variables(self):
    ld_library_path = os.environ.get('LD_LIBRARY_PATH', '')

    if not str(_AWS_LIB_PATH) in ld_library_path:
      os.environ['LD_LIBRARY_PATH'] = f'{_AWS_LIB_PATH}:{ld_library_path}'

    os.environ['FONTCONFIG_PATH'] = str(_AWS_LIB_PATH.parent)

  def get_screenshot_path(self):
    return self.screenshot_path

  def execute(self, bot):
    self._extract_chromium()
    self._set_environment_variables()

    with playwright.sync_playwright() as api:
      browser = None
      page = None

      try:
        browser = api.chromium.launch(_CHROMIUM_BINARY_PATH, _CHROMIUM_ARGS)
        page = browser.newPage()

        page.setDefaultNavigationTimeout(_NAVIGATION_TIMEOUT_MS)
        response = bot(page)

        browser.close()
        return response
      except:
        if page:
          self.screenshot_path.parent.mkdir(0o755, True, True)
          page.screenshot(path=self.screenshot_path)

        if browser:
          browser.close()

        raise
