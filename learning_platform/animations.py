from PyQt5.QtCore import QPropertyAnimation, QRect

def animate_widget(widget):
    anim = QPropertyAnimation(widget, b"geometry")
    r = widget.geometry()
    anim.setDuration(250)
    anim.setStartValue(QRect(r.x(), r.y()+40, r.width(), r.height()))
    anim.setEndValue(r)
    anim.start()
    widget.animation = anim
