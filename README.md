# Browz

A small linux application to select a browser every time you click a url. This is especially useful if you have multiple browsers or browser profiles and you want to be able to open certain links in certain browsers. Useful for web developers and others.

GNU/Linux alternative to apps such as Braus/Choosy/Browserchooser

#### Build instructions

```bash
meson build --prefix=/usr
cd build
ninja
ninja install
```

When you run `browz` for the first time, it will ask you whether you want to set it as your default browser. *Ideally you should make it default to actually get the benefit of an app like this.*

---------------

© 2020 Kavya Gokul

© 2024 Andrew D. Anderson

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
