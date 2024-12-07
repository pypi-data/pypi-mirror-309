# LocalLeaf

This tool provides an easy way to synchronize Overleaf projects from and to your local computer. No paid account necessary.

## Features
- Sync your locally modified `.tex` (and other) files to your Overleaf projects
- Sync your remotely modified `.tex` (and other) files to computer
- Works with free Overleaf account
- No Git or Dropbox required
- Does not steal or store your login credentials (works with a persisted cookie, logging in is done on the original Overleaf website)

## How To Use
### Install
TODO

### Prerequisites
- Create your project on [Overleaf](https://www.overleaf.com/project), for example a project named `test`. localleaf is not able to create projects (yet).
- Create a folder, preferably with the same name as the project (`test`) on your computer.
- Execute the script from that folder (`test`).
- If you do not specify the project name, localleaf uses the current folder's name as the project name.

### Usage
#### Login
```
lleaf login [--path]
Login successful. Cookie persisted as `.olauth`. You may now sync your project.
```

Logging in will be handled by a mini web browser opening on your device (using Qt5). You can then enter your username and password securely on the official Overleaf website. You might get asked to solve a CAPTCHA in the process. Your credentials are sent to Overleaf over HTTPS.

It then stores your *cookie* (**not** your login credentials) in a hidden file called `.olauth` in the same folder you run the command from. It is possible to store the cookie elsewhere using the `--path` option. The cookie file will not be synced to or from Overleaf.

Keep the `.olauth` file save, as it can be used to log in into your account.

### Listing all projects
```
lleaf list [--store-path -v/--verbose]
10/31/2021, 01:23:45 - Project A
09/21/2020, 01:23:45 - Project B
08/11/2019, 01:23:45 - Project C
07/01/2018, 01:23:45 - Project D
```

Use `lleaf list` to conveniently list all projects in your account available for syncing. 

### Downloading project's PDF
```
lleaf download [--name --download-path --store-path -v/--verbose]
```

Use `lleaf download` to compile and download your project's PDF. Specify a download path if you do not want to store the PDF file in the current folder. Currently only downloads the first PDF file it finds.

### Pulling changes
TODO

### Pushing changes
TODO

## Known Bugs
- When modifying a file on Overleaf and immediately syncing afterwards, the tool might not detect the changes. Please allow 1-2 minutes after modifying a file on Overleaf before syncing it to your local computer.

## Contributing

All pull requests and change/feature requests are welcome.

## Disclaimer
THE AUTHOR OF THIS SOFTWARE AND THIS SOFTWARE IS NOT ENDORSED BY, DIRECTLY AFFILIATED WITH, MAINTAINED, AUTHORIZED, OR SPONSORED BY OVERLEAF OR WRITELATEX LIMITED. ALL PRODUCT AND COMPANY NAMES ARE THE REGISTERED TRADEMARKS OF THEIR ORIGINAL OWNERS. THE USE OF ANY TRADE NAME OR TRADEMARK IS FOR IDENTIFICATION AND REFERENCE PURPOSES ONLY AND DOES NOT IMPLY ANY ASSOCIATION WITH THE TRADEMARK HOLDER OF THEIR PRODUCT BRAND.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

THIS SOFTWARE WAS DESIGNED TO BE USED ONLY FOR RESEARCH PURPOSES. THIS SOFTWARE COMES WITH NO WARRANTIES OF ANY KIND WHATSOEVER. USE IT AT YOUR OWN RISK! IF THESE TERMS ARE NOT ACCEPTABLE, YOU AREN'T ALLOWED TO USE THE CODE.

