# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import subprocess
from qtile_extras.widget.decorations import RectDecoration
from qtile_extras import widget
from qtile_extras.resources import wallpapers
from qtile_extras.popup.toolkit import(
        PopupRelativeLayout,
        PopupWidget
)
from libqtile import bar, layout, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

mod = "mod4"
terminal = guess_terminal()


@hook.subscribe.startup
def autostart():
    subprocess.Popen(['/home/robert/.config/autostart.sh'])


@hook.subscribe.startup_once
def autostart_once():
    subprocess.Popen(['/home/robert/.config/autostart_once.sh'])

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "r", lazy.spawn("/home/robert/.config/rofi/launchers/type-1/launcher.sh")),
    Key([mod], "space", lazy.window.toggle_floating()),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    #Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    Key([mod, "shift"], "s", lazy.spawn("/home/robert/.config/screenshot.sh"))
]

groups = [Group(name="1", label=""),
          Group(name="2", label=""),
          Group(name="3", label=""),
          Group(name="4", label=""),
          Group(name="5", label=""),
          Group(name="6"),
          Group(name="7"),
          Group(name="8"),
          Group(name="9")]

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

layouts = [
    layout.Columns(margin=[10, 10, 0, 10], border_width=0),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(border_width=0, margin=[10, 10, 0, 10], align=MonadTall._left),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="Source Code Pro Semibold",
    fontsize=12,
    padding=3
)
extension_defaults = widget_defaults.copy()

rect_dec = {
        "decorations":[
            RectDecoration(colour="#000000", radius=15, filled=True, clip=True)]}
rect_group = {
        "decorations":[
            RectDecoration(colour="#000000", radius=15, filled=True, group=True, clip=True)
            ]
        }
screens = [
    Screen(
        bottom=bar.Bar(
            [
                widget.Spacer(length=12, **rect_group),
                widget.GroupBox(**rect_group),
                widget.Spacer(length=12, **rect_group),
                widget.Spacer(length=bar.STRETCH),
                widget.Spacer(length=12, **rect_group),
                widget.TaskList(padding_x=5, border='#FFFFFF', **rect_group),
                widget.Spacer(length=12, **rect_group),
                widget.Spacer(length=bar.STRETCH),
                widget.Spacer(length=12, **rect_group),
                widget.WidgetBox(
                    widgets = [
                        widget.Clock(format="%Y-%m-%d %a %I:%M %p", **rect_group)
                    ],
                    text_closed = "",
                    text_open = " ",
                    close_button_location = "right",
                    **rect_group
                ),
                #widget.Clock(format="%Y-%m-%d %a %I:%M %p", **rect_group),
                widget.Spacer(length=5, **rect_group),
                widget.CheckUpdates(distro="Arch_yay", **rect_group, no_update_string='No Updates'),

                widget.Spacer(length=12, **rect_group),
                widget.Spacer(length=5),
                widget.Spacer(length=12, **rect_group),
                #widget.WidgetBox(widgets=[
                #    widget.Systray(background="#000000", padding=2, **rect_group),
                #    widget.Spacer(length=2, **rect_group)
                #    ],
                #                 close_button_location="right",
                #                 **rect_group,
                #                 text_closed="+",
                #                 text_open=""
                #    ),
                widget.StatusNotifier(**rect_group, padding=5),
                widget.TextBox(
                    fmt="",
                    mouse_callbacks = {
                        "Button1": lazy.spawn("/home/robert/.config/rofi/launchers/type-1/powermenu.sh")
                    },
                    **rect_group),
                widget.Spacer(length=12, **rect_group)
            ],
            30,
            margin=10,
            background="#00000000",
        ),
        wallpaper = wallpapers.WALLPAPER_TRIANGLES,
        wallpaper_mode = "fill"
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
