from manim import *  # or: from manimlib import *
from manim_slides import Slide

class FakeLine(Rectangle):
    def __init__(self, start, end, **kwargs):
        super().__init__(width=0, height=0, **kwargs)
        line = Line(start, end, **kwargs)
        fake_line = (Rectangle(height=0.001, width=line.get_length())
            .move_to(line.get_start(), aligned_edge=LEFT)
            .rotate(line.get_angle(), about_point=line.get_start())
            )        
        self.set_points(fake_line.points)

def Myintersection(vmobj1, vmobj2):
    def find_extremes(path):
        result = []
        i = 0
        while i < len(path):
            prev, p1 = path[i-1], path[i]
            if np.linalg.norm(p1-prev) < 0.002:
                result.append(p1)
                i += 4
            i += 4
        return result
    
    def find_candidates(vmobj):
        result = []
        for points in vmobj.get_subpaths():
            result.extend(find_extremes(points))
        return result

    if isinstance(vmobj1, Line):
        line = vmobj1
        if isinstance(vmobj1, Line):
            vmobj =  FakeLine(*vmobj2.get_start_and_end())
        else :
            vmobj = vmobj2
        fake_line = FakeLine(*line.get_start_and_end())
    elif isinstance(vmobj2, Line):
        line = vmobj2
        vmobj = vmobj1
        fake_line = FakeLine(*line.get_start_and_end())
    else:
        raise ValueError("At least one of the objects must be a line")
    
    segment = Difference(fake_line, vmobj)
    if segment:
        candidates = sorted(find_candidates(segment),
                key=lambda p: np.linalg.norm(p-line.get_start()))
        return candidates[1:-1]  # Remove the start and end of the line
    else:
        return []


def MyLabeledDot(label_in:Tex| None = None,label_out:Tex| None = None,pos:Vector = DOWN,shift=[0,0,0], point=ORIGIN,radius: float = DEFAULT_DOT_RADIUS,color = WHITE):
        if isinstance(label_in, Tex):
            radius = 0.02 + max(label_in.width, label_in.height) / 2
        
        dot = Dot(point=point,radius=radius,color=color)
        g1 = VGroup(dot)
        if isinstance(label_in, Tex):
            label_in.move_to(dot.get_center())
            g1.add(label_in)
        if isinstance(label_out, Tex):
            label_out.next_to(dot,pos)
            label_out.shift(shift)
            g1.add(label_out)

        return g1


class MyDashLabeledLine(DashedLine):
    def __init__(self,label: Tex|MathTex, pos = None, rel_pos: float = 0.5,bg = BLACK, opacity:float= 0.7,rot: bool =True  , *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        # calculating the vector for the label position
        line_start, line_end = self.get_start_and_end()
        new_vec = (line_end - line_start) * rel_pos
        label_coords = line_start + new_vec
        label.move_to(label_coords)
        
        if rot:
            ang=angle_of_vector(self.get_unit_vector())
            if ang < -PI/2:
                ang =  ang+PI
            elif ang > PI/2:
                ang=ang-PI

            label.rotate(ang)

        if pos is None:
            mask  = Line(label.get_center()-0.6*label.width*self.get_unit_vector(),label.get_center()+0.6*label.width*self.get_unit_vector(),color=bg,stroke_width=self.get_stroke_width()+1,stroke_opacity=opacity)
            self.add(mask)
        else:
            label.shift(pos)
        self.add(label)

class MyLabeledLine(Line):
    def __init__(self,label: Tex|MathTex, pos = None, rel_pos: float = 0.5,bg = BLACK, opacity:float= 0.7,rot: bool =True , *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        # calculating the vector for the label position
        line_start, line_end = self.get_start_and_end()
        new_vec = (line_end - line_start) * rel_pos
        label_coords = line_start + new_vec
        label.move_to(label_coords)
        if pos is None:
            if rot:
                mask  = Line(label.get_center()-0.65*label.width*self.get_unit_vector(),label.get_center()+0.65*label.width*self.get_unit_vector(),color=bg,stroke_width=self.get_stroke_width()+1,stroke_opacity=opacity)
            else:
                mask  = Line(label.get_center()-0.65*label.height*self.get_unit_vector(),label.get_center()+0.65*label.height*self.get_unit_vector(),color=bg,stroke_width=self.get_stroke_width()+1,stroke_opacity=opacity)
            self.add(mask)
        else:
            label.shift(pos)
        
        if rot:
            ang=angle_of_vector(self.get_unit_vector())
            if ang < -PI/2:
                ang =  ang+PI
            elif ang > PI/2:
                ang=ang-PI

            label.rotate(ang)
        self.add(label)


class MyLabeledArrow(MyLabeledLine, Arrow):

    def __init__(
        self,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(buff=0,*args, **kwargs)

class MyDoubLabArrow(MyLabeledLine, DoubleArrow):

    def __init__(
        self,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(buff=0,*args, **kwargs)


def Item(*str,dot = True,font_size = 35,math=False,pw="8cm",color=WHITE):
    if math:
        tex = MathTex(*str,font_size=font_size,color=color)
    else:
        tex = Tex(*str,color=color,font_size=font_size,tex_environment=f"{{minipage}}{{{pw}}}")

    if dot:
        dot = MathTex("\\cdot").scale(2)
        dot.next_to(tex[0][0], LEFT, SMALL_BUFF)
        tex[0].add_to_back(dot)
    else:
        dot = MathTex("\\cdot",color=BLACK).scale(2)
        dot.next_to(tex[0], LEFT, SMALL_BUFF)
        tex[0].add_to_back(dot)
    g2 = VGroup()
    for item in tex:
        g2.add(item)

    return(g2)


def ItemList(*item,buff=MED_SMALL_BUFF):
    list = VGroup(*item).arrange(DOWN, aligned_edge=LEFT,buff=buff)
    return(list)


def ir(a,b): # inclusive range, useful for TransformByGlyphMap
    return list(range(a,b+1))


class LatexItems(Tex):
    def __init__(self, *args, page_width="15em", itemize="itemize",font_size=35, **kwargs):
        template = TexTemplate()
        template.body = (r"\documentclass[preview]{standalone}\usepackage[english]{babel}"
                         r"\usepackage{amsmath}\usepackage{amssymb}\begin{document}"
                         rf"\begin{{minipage}}{{{page_width}}}"
                         rf"\begin{{{itemize}}}YourTextHere\end{{{itemize}}}"
                         r"\end{minipage}\end{document}"
        )
        super().__init__(*args, tex_template=template, tex_environment=None,font_size=font_size, **kwargs)


class AlignTex(Tex):
    def __init__(self, *args, page_width="15em",align="align*",font_size=35, **kwargs):
        template = TexTemplate()
        template.body = (r"\documentclass[preview]{standalone}\usepackage[english]{babel}"
                         r"\usepackage{amsmath}\usepackage{amssymb}\usepackage{cancel}\begin{document}"
                         rf"\begin{{minipage}}{{{page_width}}}"
                         rf"\begin{{{align}}}YourTextHere\end{{{align}}}"
                         r"\end{minipage}\end{document}"
        )
        super().__init__(*args,font_size=font_size, tex_template=template, tex_environment=None, **kwargs)


class TransformByGlyphMap(AnimationGroup):
    def __init__(self, mobA, mobB, *glyph_map, replace=True, from_copy=True, show_indices=False, **kwargs):
		# replace=False does not work properly
        if from_copy:
            self.mobA = mobA.copy()
            self.replace = True
        else:
            self.mobA = mobA
            self.replace = replace
        self.mobB = mobB
        self.glyph_map = glyph_map
        self.show_indices = show_indices

        animations = []
        mentioned_from_indices = []
        mentioned_to_indices = []
        for from_indices, to_indices in self.glyph_map:
            print(from_indices, to_indices)
            if len(from_indices) == 0 and len(to_indices) == 0:
                self.show_indices = True
                continue
            elif len(to_indices) == 0:
                animations.append(FadeOut(
                    VGroup(*[self.mobA[0][i] for i in from_indices]),
                    shift = self.mobB.get_center()-self.mobA.get_center()
                ))
            elif len(from_indices) == 0:
                animations.append(FadeIn(
                    VGroup(*[self.mobB[0][j] for j in to_indices]),
                    shift = self.mobB.get_center() - self.mobA.get_center()
                ))
            else:
                animations.append(Transform(
                    VGroup(*[self.mobA[0][i].copy() if i in mentioned_from_indices else self.mobA[0][i] for i in from_indices]),
                    VGroup(*[self.mobB[0][j] for j in to_indices]),
                    replace_mobject_with_target_in_scene=self.replace
                ))
            mentioned_from_indices.extend(from_indices)
            mentioned_to_indices.extend(to_indices)

        print(mentioned_from_indices, mentioned_to_indices)
        remaining_from_indices = list(set(range(len(self.mobA[0]))) - set(mentioned_from_indices))
        remaining_from_indices.sort()
        remaining_to_indices = list(set(range(len(self.mobB[0]))) - set(mentioned_to_indices))
        remaining_to_indices.sort()
        print(remaining_from_indices, remaining_to_indices)
        if len(remaining_from_indices) == len(remaining_to_indices) and not self.show_indices:
            for from_index, to_index in zip(remaining_from_indices, remaining_to_indices):
                animations.append(Transform(
                    self.mobA[0][from_index],
                    self.mobB[0][to_index],
                    replace_mobject_with_target_in_scene=self.replace
                ))
            super().__init__(*animations, **kwargs)
        else:
            print(f"From indices: {len(remaining_from_indices)}    To indices: {len(remaining_to_indices)}")
            print("Showing indices...")
            super().__init__(
                Create(index_labels(self.mobA[0], color=PINK)),
                FadeIn(self.mobB.next_to(self.mobA, DOWN), shift=DOWN),
                Create(index_labels(self.mobB[0], color=PINK)),
                Wait(5),
                lag_ratio=0.5
                )
            
def Ray(start,end,ext:float=0,eext:float = 0,pos:float=0.5,color=BLUE):
    dir_lin = Line(start=start,end=end)
    dir = dir_lin.get_length()*ext*dir_lin.get_unit_vector()
    edir = dir_lin.get_length()*eext*dir_lin.get_unit_vector()
    lin = Line(start=start-edir,end=end+dir,color=color)
    arrow_start = lin.get_start()+pos*lin.get_length()*lin.get_unit_vector()
    arrow = Arrow(start=arrow_start-0.1*lin.get_unit_vector(),end=arrow_start+0.1*lin.get_unit_vector(),tip_shape=StealthTip,max_tip_length_to_length_ratio=0.75,color=color)
    ray = VGroup(lin,arrow)
    return ray

def DashRay(start,end,ext:float=0,color=DARK_BROWN):
    dir_lin = Line(start=start,end=end)
    dir = dir_lin.get_length()*ext*dir_lin.get_unit_vector()
    ray = DashedLine(start=start,end=end+dir,color=color)
    return ray

def PlaneMirror():
    # Creating convex mirror
        a2=Line(start=2*UP,end=2*DOWN,color=GREEN)
        mirror=VGroup(a2)
        for point in range(0,11):
            mirror.add(Line([0,-2+0.4*point,0],[0.1,-2+0.4*point+0.1,0],color=GREEN))

        mirror.move_to(ORIGIN+RIGHT)
        pol_cord = a2.get_center()
        return [mirror,pol_cord]

def Convex(R=6, sa=160,ang=40,dash=0.025,pas=0.75,pae=0.1):
    # Creating convex mirror
        a2=Arc(R,start_angle=sa*DEGREES,angle= ang*DEGREES,arc_center=[0,0,0],color=GREEN)
        mirror=VGroup(a2)
        for point in a2.get_all_points():
            mirror.add(Line(point,point-dash*point,color=GREEN))

        mirror.move_to(ORIGIN+RIGHT)
        pol_cord = a2.get_left()
        cent_cord = a2.get_arc_center()
        foc_cord =  0.5*(pol_cord+cent_cord)
        rad = a2.radius
        foc_len = rad/2

        # Creating Principal axis, pole, center of curvature and focus
        pa = VGroup(Line(pol_cord+pas*rad*LEFT,cent_cord+pae*rad*RIGHT))
        dash = Dot(color=RED) #Line(start=0.1*DOWN,end=0.1*UP)
        cen = VGroup(dash.copy().move_to(cent_cord),Tex("C",font_size=30).move_to(cent_cord+0.25*DOWN))
        pol = VGroup(dash.copy().move_to(pol_cord),Tex("P",font_size=30).move_to(pol_cord+0.25*DOWN))
        foc = VGroup(dash.copy().move_to(foc_cord),Tex("F",font_size=30).move_to(foc_cord+0.25*DOWN))
        pa.add(pol,cen,foc)
        return [mirror,pa,pol_cord,cent_cord,foc_cord,rad,foc_len]

def Concave(R=6,sa=20,ang=-40,dash=0.025,pae=0.65, pas=0.5):
    # Creating convex mirror
        a2=Arc(R,start_angle=sa*DEGREES,angle= ang*DEGREES,arc_center=[0,0,0],color=GREEN)
        mirror=VGroup(a2)
        for point in a2.get_all_points():
            mirror.add(Line(point,point+dash*point,color=GREEN))

        pol_cord = a2.get_right()
        cent_cord = a2.get_arc_center()
        foc_cord =  0.5*(pol_cord+cent_cord)
        rad = a2.radius
        foc_len = rad/2

        # Creating Principal axis, pole, center of curvature and focus
        pa = VGroup(Line(pol_cord+pae*rad*RIGHT,cent_cord+pas*rad*LEFT))
        dash = Dot(color=RED) #Line(start=0.1*DOWN,end=0.1*UP)
        cen = VGroup(dash.copy().move_to(cent_cord),Tex("C",font_size=30).move_to(cent_cord+0.25*DOWN))
        pol = VGroup(dash.copy().move_to(pol_cord),Tex("P",font_size=30).move_to(pol_cord+0.25*DOWN+0.1*LEFT))
        foc = VGroup(dash.copy().move_to(foc_cord),Tex("F",font_size=30).move_to(foc_cord+0.25*DOWN))
        pa.add(pol,cen,foc)
        return [mirror,pa,pol_cord,cent_cord,foc_cord,rad,foc_len]

def ConvexLens(R=6,pas=0.1,pae=0.1,c1 = True, c2=True,pos=0,f1=True,f2=True,o=True,l=True):
    sph1 = Circle(R,fill_color=BLUE_D,fill_opacity=0.2).shift(-(R-0.18)*RIGHT)
    sph2 = Circle(R,fill_color=BLUE_D,fill_opacity=0.2).shift((R-0.18)*RIGHT)
    lens = Intersection(sph1,sph2,fill_color=BLUE_D,fill_opacity=0.6,stroke_width=1)
    f = (sph2.get_center()+lens.get_center())/2
    # Creating Principal axis, pole, center of curvature and focus
    line = Line(sph1.get_center()+pas*R*LEFT,sph2.get_center()+pae*R*RIGHT)
    pa = VGroup()
    dash = Dot(color=RED,radius=0.05) #Line(start=0.1*DOWN,end=0.1*UP)
    C1 = VGroup(dash.copy().move_to(sph1.get_center()),Tex(r"$C_1$\\$(2F_1)$",font_size=30).move_to(sph1.get_center()+0.5*DOWN))
    C2 = VGroup(dash.copy().move_to(sph2.get_center()),Tex(r"$C_2$\\$(2F_2)$",font_size=30).move_to(sph2.get_center()+0.5*DOWN))
    O = VGroup(dash.copy().move_to(lens.get_center()),Tex("O",font_size=30).move_to(lens.get_center()+0.25*DOWN))
    F1 = VGroup(dash.copy().move_to(-f),Tex(r"$F_1$",font_size=30).move_to(-f+0.25*DOWN))
    F2 = VGroup(dash.copy().move_to(f),Tex(r"$F_2$",font_size=30).move_to(f+0.25*DOWN))
    VGroup(sph1,sph2,lens,pa,C1,C2,O,F1,F2).shift(pos*RIGHT)
    if l:
        pa.add(line)
    if c1:
        pa.add(C1)
    if c2:
        pa.add(C2)
    if f1:
        pa.add(F1)
    if f2:
        pa.add(F2)
    if o:
        pa.add(O)
    return [lens,pa,f,sph1,sph2]

def ConcaveLens(R=6,pas=0.1,pae=0.1,c1 = True, c2=True,pos=0,f1=True,f2=True,o=True,l=True):
    sph1 = Circle(R,fill_color=BLUE_D,fill_opacity=0.2).shift(-(R+0.09)*RIGHT)
    sph2 = Circle(R,fill_color=BLUE_D,fill_opacity=0.2).shift((R+0.09)*RIGHT)
    rect = Rectangle(height=2*np.sqrt( 0.18*(2*R-0.18)),width=2,fill_opacity=0.6)
    lens =  Difference(Difference(rect,sph1),sph2,fill_color=BLUE_D,fill_opacity=0.6,stroke_width=1)
    f = (sph2.get_center()+lens.get_center())/2
    # Creating Principal axis, pole, center of curvature and focus
    line = Line(sph1.get_center()+pas*R*LEFT,sph2.get_center()+pae*R*RIGHT)
    pa = VGroup()
    dash = Dot(color=RED,radius=0.05) #Line(start=0.1*DOWN,end=0.1*UP)
    C1 = VGroup(dash.copy().move_to(sph1.get_center()),Tex(r"$C_1$\\$(2F_1)$",font_size=30).move_to(sph1.get_center()+0.5*DOWN))
    C2 = VGroup(dash.copy().move_to(sph2.get_center()),Tex(r"$C_2$\\$(2F_2)$",font_size=30).move_to(sph2.get_center()+0.5*DOWN))
    O = VGroup(dash.copy().move_to(lens.get_center()),Tex("O",font_size=30).move_to(lens.get_center()+0.25*DOWN))
    F1 = VGroup(dash.copy().move_to(-f),Tex(r"$F_1$",font_size=30).move_to(-f+0.25*DOWN))
    F2 = VGroup(dash.copy().move_to(f),Tex(r"$F_2$",font_size=30).move_to(f+0.25*DOWN))
    VGroup(sph1,sph2,lens,pa,C1,C2,O,F1,F2).shift(pos*RIGHT)
    if l:
        pa.add(line)
    if c1:
        pa.add(C1)
    if c2:
        pa.add(C2)
    if f1:
        pa.add(F1)
    if f2:
        pa.add(F2)
    if o:
        pa.add(O)
    return [lens,pa,f,sph1,sph2]

def PlanoConvexLens(R=6):
    sph2 = Circle(R,fill_color=BLUE_D,fill_opacity=0.6).shift((R+0.09)*RIGHT)
    rect = Rectangle(height=3,width=0.99,fill_opacity=0.6)
    lens =  Intersection(rect,sph2,fill_color=BLUE_D,fill_opacity=0.6,stroke_width=1)
    return(lens,rect,sph2)

def PlanoConcaveLens(R=6):
    sph2 = Circle(R,fill_color=BLUE_D,fill_opacity=0.6).shift((R-0.09)*RIGHT)
    rect = Rectangle(height=3,width=0.72,fill_opacity=0.6)
    lens =  Difference(rect,sph2,fill_color=BLUE_D,fill_opacity=0.6,stroke_width=1)
    return(lens,rect,sph2)


class Refraction(Slide):
    def construct(self):
        title = Title('CHAPTER 1 : LIGHT REFLECTION AND REFRACTION',color=GREEN,match_underline_width_to_text=True)
        self.add(title)
        Outline = Tex('Learning Objectives :',color=BLUE,font_size=35).next_to(title,DOWN).to_corner(LEFT,buff=0.1)
        self.add(Outline)
        list = BulletedList('Introduction',' Reflection And Laws of reflection','Spherical Mirrors','Image formation by Spherical Mirrors','Ray Diagrams','Uses of Concave and Convex Mirrors',
                            'Sign Convention','Mirror Formula and Magnification',font_size=35).next_to(Outline,DOWN).align_to(Outline,LEFT)

        list2 = BulletedList('Refraction of Light','Refraction through a Rectangular Glass Slab','Laws of Refraction','The Refractive Index',
                             'Refraction by Spherical Lenses',' Image Formation by Lenses \& Ray Diagrams',"Lens Formula \& Magnification","Power of a Lens",font_size=35).next_to(Outline,DOWN).next_to(list,RIGHT).align_to(list,UP)

        self.add(list,list2)
        self.next_slide(loop=True)
        self.play(FocusOn(list2[0]))
        self.play(Circumscribe(list2[0]))
        self.next_slide()
        self.play(RemoveTextLetterByLetter(list2))
        self.play(RemoveTextLetterByLetter(list))
        self.play(RemoveTextLetterByLetter(Outline))
        Intro_title = Title('Refraction of Light', color=GREEN,match_underline_width_to_text=True,underline_buff=0.15)
        self.play(ReplacementTransform(title,Intro_title))
        self.next_slide()


        steps = ItemList(Item(r"When traveling obliquely from one medium to another, the direction of propagation of light in the second medium changes. This phenomenon is known as refraction of light.",pw="7.5 cm"),
                         Item(r" OR ",pw="7.5 cm",dot=False,color=RED),
                         Item(r"The bending of light when it enters obliquely from one transparent medium to another.",pw="7.5 cm"),
                         Item(r"The major cause of refraction to occur is the change in the speed of light in different mediums",pw="7.5 cm"),
                         Item(r"Speed of light is maximum in vacuum : $c= 3\times 10^8$ m/s",pw="13 cm"),
                         Item(r"Fermat's Principle : ", r"A ray of light going from point A to point B always takes the route of least time.",pw="13 cm"),
                        buff=0.4).next_to(Intro_title,DOWN,buff=0.15).to_corner(LEFT,buff=0.1)
        
        steps[5][0].set_color(GOLD)
        
        slab_img = ImageMobject("slab.png").scale(0.8).next_to(steps[0],RIGHT).align_to(steps,UP)

        ex_title = Tex("Some Examples of Refraction :",color=BLUE).next_to(Intro_title,DOWN).to_corner(LEFT)
        ul = Underline(ex_title)
        examples = ItemList(Item(r"(1) ", r"The bottom of swimming pool appears higher",pw="7.5 cm"),
                         Item(r"(2) ", r"The pencil partially immersed in water appears to be bent at the interface.",pw="7.5 cm"),
                         Item(r"(3) ", r"Lemons placed in a glass tumbler appears bigger.",pw="7.5 cm"),
                         Item(r"(4) ", r"Letters of a book appear to be raised when seen through a glass slab.",pw="7.5 cm"),
                        buff=0.5).next_to(ex_title,DOWN,buff=0.5).to_corner(LEFT,buff=0.1)
        
        pool_img = ImageMobject("pool.jpg").scale(0.7).next_to(examples,RIGHT).align_to(ex_title,UP)
        pencil_img = ImageMobject("pencil2.jpg").next_to(examples,RIGHT).align_to(ex_title,UP)
        lemons_img = ImageMobject("lemons.jpg").next_to(examples,RIGHT).align_to(ex_title,UP)
        letters_img = ImageMobject("letters.webp").scale(3).next_to(examples,RIGHT).align_to(ex_title,UP)

        img_group = Group(pool_img,pencil_img,lemons_img,letters_img)

        self.play(FadeIn(slab_img))
        for item in steps:
            self.play(Write(item))
            self.next_slide()
        self.play(FadeOut(slab_img,steps),Write(VGroup(ex_title,ul)))
        self.next_slide()
        for i in range(4):
            examples[i][0].set_color(GOLD)
            self.play(Write(examples[i]),FadeIn(img_group[i]))
            self.next_slide()
            self.play(FadeOut(img_group[i]))
            self.wait(1)


class GlassSlab(Slide):
    def construct(self):
        title = Title('CHAPTER 1 : LIGHT REFLECTION AND REFRACTION',color=GREEN,match_underline_width_to_text=True)
        self.add(title)
        Outline = Tex('Learning Objectives :',color=BLUE,font_size=35).next_to(title,DOWN).to_corner(LEFT,buff=0.1)
        self.add(Outline)
        list = BulletedList('Introduction',' Reflection And Laws of reflection','Spherical Mirrors','Image formation by Spherical Mirrors','Ray Diagrams','Uses of Concave and Convex Mirrors',
                            'Sign Convention','Mirror Formula and Magnification',font_size=35).next_to(Outline,DOWN).align_to(Outline,LEFT)

        list2 = BulletedList('Refraction of Light','Refraction through a Rectangular Glass Slab','Laws of Refraction','The Refractive Index',
                             'Refraction by Spherical Lenses',' Image Formation by Lenses \& Ray Diagrams',"Lens Formula \& Magnification","Power of a Lens",font_size=35).next_to(Outline,DOWN).next_to(list,RIGHT).align_to(list,UP)

        self.add(list,list2)
        self.next_slide(loop=True)
        self.play(FocusOn(list2[1]))
        self.play(Circumscribe(list2[1]))
        self.next_slide()
        self.play(RemoveTextLetterByLetter(list2))
        self.play(RemoveTextLetterByLetter(list))
        self.play(RemoveTextLetterByLetter(Outline))
        Intro_title = Title('Refraction through a Rectangular Glass Slab', color=GREEN,match_underline_width_to_text=True,underline_buff=0.15)
        self.play(ReplacementTransform(title,Intro_title))
        self.next_slide()

        slab = Rectangle(BLUE,height=3,width=5,fill_opacity=0.5,fill_color=BLUE)
        slab_lbl = Tex(r"Glass",font_size=35).move_to(1.2*UP+2*RIGHT)
        air_lbl = Tex(r"Air",font_size=35).move_to(2*UP+2*RIGHT)
        normal_1 = DashedLine(start=1.5*LEFT+2.5*UP,end=1.5*LEFT+0.5*UP,color=GREY_BROWN)
        normal_2 = DashedLine(start=0.5*DOWN,end=2.5*DOWN,color=GREY_BROWN)
        i_ray = Ray(start=3*LEFT+3*UP,end=1.5*LEFT+1.5*UP,color=RED)
        r_ray = Ray(start=1.5*LEFT+1.5*UP,end=1.5*DOWN,color=RED)
        e_ray = Ray(start=1.5*DOWN,end=1.5*DOWN+2*i_ray[0].get_unit_vector(),color=RED)
        ext_ray = DashedLine(start=1.5*LEFT+1.5*UP,end=1.5*LEFT+1.5*UP+5.2*i_ray[0].get_unit_vector(),color=LIGHT_BROWN)
        i_ang = Angle(normal_1,i_ray[0],radius=0.5,quadrant=(-1,-1),color=YELLOW)
        r_ang = Angle(normal_1,r_ray[0],radius=0.5,quadrant=(1,1),color=YELLOW)
        e_ang = Angle(normal_2,e_ray[0],radius=0.5,quadrant=(1,1),color=YELLOW)
        i_lbl = Tex(r"$\angle i$",font_size=30).next_to(i_ang,UP,buff=0.1)
        r_lbl = Tex(r"$\angle r$",font_size=30).next_to(r_ang,DOWN,buff=0.1)
        e_lbl = Tex(r"$\angle e$",font_size=30).next_to(e_ang,DOWN,buff=0.1)
        i_arrow  = CurvedArrow(start_point=i_ray[0].get_start(),end_point=i_ray[0].get_start()-0.3*DOWN+RIGHT,color=GOLD,tip_length=0.1)
        i_arrow_lbl = Tex("Incident Ray",font_size=30,color=GOLD).move_to(i_arrow.get_end())
        n_arrow  = CurvedArrow(start_point=normal_1.get_start(),end_point=normal_1.get_start()-0.3*DOWN+1.5*RIGHT,color=GREEN,tip_length=0.1)
        n_arrow_lbl = Tex("Normal",font_size=30,color=GOLD).move_to(n_arrow.get_end()).shift(0.1*UP)

        r_arrow  = CurvedArrow(start_point=r_ray[0].get_all_points()[2],end_point=r_ray[0].get_all_points()[2]+0.4*DOWN+1.5*LEFT,color=GREEN,tip_length=0.1)
        r_arrow_lbl = Tex("Refracted Ray",font_size=30,color=GOLD).move_to(r_arrow.get_end()).shift(0.1*DOWN)

        e_arrow  = CurvedArrow(start_point=e_ray[0].get_all_points()[3],end_point=e_ray[0].get_all_points()[3]+1*LEFT,color=GREEN,tip_length=0.1)
        e_arrow_lbl = Tex("Emergent Ray",font_size=30,color=GOLD).move_to(e_arrow.get_end()).shift(0.1*DOWN)

        d_arrow = MyDoubLabArrow(label=Tex(r"$d$",font_size=30),start=e_ray[0].get_end(),end=ext_ray.get_end(),tip_length=0.1)


        img = VGroup(slab,slab_lbl,air_lbl,normal_1,n_arrow,n_arrow_lbl,i_ray,i_arrow,i_arrow_lbl,i_ang,i_lbl,r_ray,r_arrow,r_arrow_lbl,r_ang,r_lbl,normal_2,e_ray,e_arrow,e_arrow_lbl,e_ang,e_lbl,ext_ray,d_arrow).next_to(Intro_title,DOWN).to_corner(RIGHT)
        for item in img:
            self.play(Write(item))
            self.wait(3)
        steps = ItemList(Item(r"The extent of bending of a ray of light at the opposite parallel faces of a rectangular glass slab is equal and opposite, ", r"so the ray emerges parallel to incident ray.",pw="7.5 cm"),
                         Item(r"For glass slab : $\angle i=\angle e$",pw="7.5 cm"),
                         Item(r"The perpendicular distance between direction of incident ray and emergent ray is called lateral displacement $(d)$ ",pw="7.5 cm"),
                         Item(r"Lateral displacement $(d)$ depends on - ",pw="7.5 cm"),
                         Item(r"(1) Refractive index of the material of the slab.",pw="7.5 cm",dot=False),
                         Item(r"(2) Thickness of the slab.",pw="7.5 cm",dot=False),
                         Item(r"(3) Angle of incidence.",pw="7.5 cm",dot=False),
                        buff=0.3).next_to(Intro_title,DOWN,buff=0.15).to_corner(LEFT,buff=0.2)
        
        steps[0][1].set_color(YELLOW)
        
        for item in steps:
            self.play(Write(item))
            self.next_slide()
        self.wait(2)


class LawsRefraction(Slide):
    def construct(self):
        title = Title('CHAPTER 1 : LIGHT REFLECTION AND REFRACTION',color=GREEN,match_underline_width_to_text=True)
        self.add(title)
        Outline = Tex('Learning Objectives :',color=BLUE,font_size=35).next_to(title,DOWN).to_corner(LEFT,buff=0.1)
        self.add(Outline)
        list = BulletedList('Introduction',' Reflection And Laws of reflection','Spherical Mirrors','Image formation by Spherical Mirrors','Ray Diagrams','Uses of Concave and Convex Mirrors',
                            'Sign Convention','Mirror Formula and Magnification',font_size=35).next_to(Outline,DOWN).align_to(Outline,LEFT)

        list2 = BulletedList('Refraction of Light','Refraction through a Rectangular Glass Slab','Laws of Refraction','The Refractive Index',
                             'Refraction by Spherical Lenses',' Image Formation by Lenses \& Ray Diagrams',"Lens Formula \& Magnification","Power of a Lens",font_size=35).next_to(Outline,DOWN).next_to(list,RIGHT).align_to(list,UP)

        self.add(list,list2)
        self.next_slide(loop=True)
        self.play(FocusOn(list2[2]))
        self.play(Circumscribe(list2[2]))
        self.next_slide()
        self.play(RemoveTextLetterByLetter(list2))
        self.play(RemoveTextLetterByLetter(list))
        self.play(RemoveTextLetterByLetter(Outline))
        Intro_title = Title('Laws of Refraction', color=GREEN,match_underline_width_to_text=True,underline_buff=0.15)
        self.play(ReplacementTransform(title,Intro_title))
        self.next_slide()

        slab = Rectangle(BLUE,height=3,width=5,fill_opacity=0.5,fill_color=BLUE)
        slab_lbl = Tex(r"Medium 2\\ (Glass)",font_size=35).move_to(1*UP+1.6*RIGHT)
        air_lbl = Tex(r"Medium 1\\ (Air)",font_size=35).move_to(2.2*UP+1.6*RIGHT)
        normal_1 = DashedLine(start=1.5*LEFT+2.5*UP,end=1.5*LEFT+0.5*UP,color=GREY_BROWN)
        normal_2 = DashedLine(start=0.5*DOWN,end=2.5*DOWN,color=GREY_BROWN)
        i_ray = Ray(start=3*LEFT+3*UP,end=1.5*LEFT+1.5*UP,color=RED)
        r_ray = Ray(start=1.5*LEFT+1.5*UP,end=1.5*DOWN,color=RED)
        e_ray = Ray(start=1.5*DOWN,end=1.5*DOWN+2*i_ray[0].get_unit_vector(),color=RED)
        ext_ray = DashedLine(start=1.5*LEFT+1.5*UP,end=1.5*LEFT+1.5*UP+5.2*i_ray[0].get_unit_vector(),color=LIGHT_BROWN)
        i_ang = Angle(normal_1,i_ray[0],radius=0.5,quadrant=(-1,-1),color=YELLOW)
        r_ang = Angle(normal_1,r_ray[0],radius=0.5,quadrant=(1,1),color=YELLOW)
        e_ang = Angle(normal_2,e_ray[0],radius=0.5,quadrant=(1,1),color=YELLOW)
        i_lbl = Tex(r"$\angle i$",font_size=30).next_to(i_ang,UP,buff=0.1)
        r_lbl = Tex(r"$\angle r$",font_size=30).next_to(r_ang,DOWN,buff=0.1)
        e_lbl = Tex(r"$\angle e$",font_size=30).next_to(e_ang,DOWN,buff=0.1)
        i_arrow  = CurvedArrow(start_point=i_ray[0].get_start(),end_point=i_ray[0].get_start()-0.3*DOWN+RIGHT,color=GOLD,tip_length=0.1)
        i_arrow_lbl = Tex("Incident Ray",font_size=30,color=GOLD).move_to(i_arrow.get_end())
        n_arrow  = CurvedArrow(start_point=normal_1.get_start(),end_point=normal_1.get_start()-0.3*DOWN+1.5*RIGHT,color=GREEN,tip_length=0.1)
        n_arrow_lbl = Tex("Normal",font_size=30,color=GOLD).move_to(n_arrow.get_end()).shift(0.1*UP)

        r_arrow  = CurvedArrow(start_point=r_ray[0].get_all_points()[2],end_point=r_ray[0].get_all_points()[2]+0.4*DOWN+1.5*LEFT,color=GREEN,tip_length=0.1)
        r_arrow_lbl = Tex("Refracted Ray",font_size=30,color=GOLD).move_to(r_arrow.get_end()).shift(0.1*DOWN)

        e_arrow  = CurvedArrow(start_point=e_ray[0].get_all_points()[3],end_point=e_ray[0].get_all_points()[3]+1*LEFT,color=GREEN,tip_length=0.1)
        e_arrow_lbl = Tex("Emergent Ray",font_size=30,color=GOLD).move_to(e_arrow.get_end()).shift(0.1*DOWN)

        d_arrow = MyDoubLabArrow(label=Tex(r"$d$",font_size=30),start=e_ray[0].get_end(),end=ext_ray.get_end(),tip_length=0.1)


        img = VGroup(slab,normal_1,i_ray,r_ray,slab_lbl,air_lbl,i_ang,r_ang,i_lbl,r_lbl).next_to(Intro_title,DOWN).to_corner(RIGHT)
        self.add(img)

        steps = ItemList(Item(r"(1) ", r" The incident ray, the refracted ray and the normal at the point of incidence all lie in the same plane.",pw="7.5 cm"),
                         Item(r"(2) Snell's law : ", r" The ratio of the sine of the angle of incidence to the sine of the angle of refraction is a constant.",pw="7.5 cm"),
                         Item(r"$\dfrac{\sin (\angle i)}{\sin(\angle r)}=\text{Constant}$ ",r"$=n_{21}$",pw="7.5 cm",color=PINK,dot=False),
                         Item(r"This ",r"constant ", r"value is called the ", r"refractive index $(n_{21})$ ", r"of the second medium with respect to the first.",pw="7.5 cm",dot=False),
                        buff=0.5).next_to(Intro_title,DOWN,buff=0.5).to_corner(LEFT,buff=0.2)
        
        sr = SurroundingRectangle(steps[2])
        VGroup(steps[3][1],steps[3][3]).set_color(YELLOW)
        steps[0][0].set_color(GOLD)
        steps[1][0].set_color(GOLD)
        
        for item in steps[0:3]:
            for subitem in item:
                self.play(Write(subitem))
                self.next_slide()

        self.play(Write(sr),Write(steps[3]))
        self.wait(2)


class RefIndex(Slide):
    def construct(self):
        title = Title('CHAPTER 1 : LIGHT REFLECTION AND REFRACTION',color=GREEN,match_underline_width_to_text=True)
        self.add(title)
        Outline = Tex('Learning Objectives :',color=BLUE,font_size=35).next_to(title,DOWN).to_corner(LEFT,buff=0.1)
        self.add(Outline)
        list = BulletedList('Introduction',' Reflection And Laws of reflection','Spherical Mirrors','Image formation by Spherical Mirrors','Ray Diagrams','Uses of Concave and Convex Mirrors',
                            'Sign Convention','Mirror Formula and Magnification',font_size=35).next_to(Outline,DOWN).align_to(Outline,LEFT)

        list2 = BulletedList('Refraction of Light','Refraction through a Rectangular Glass Slab','Laws of Refraction','The Refractive Index',
                             'Refraction by Spherical Lenses',' Image Formation by Lenses \& Ray Diagrams',"Lens Formula \& Magnification","Power of a Lens",font_size=35).next_to(Outline,DOWN).next_to(list,RIGHT).align_to(list,UP)

        self.add(list,list2)
        self.next_slide(loop=True)
        self.play(FocusOn(list2[3]))
        self.play(Circumscribe(list2[3]))
        self.next_slide()
        self.play(RemoveTextLetterByLetter(list2))
        self.play(RemoveTextLetterByLetter(list))
        self.play(RemoveTextLetterByLetter(Outline))
        Intro_title = Title('The Refractive Index', color=GREEN,match_underline_width_to_text=True,underline_buff=0.15).to_corner(UL)
        self.play(ReplacementTransform(title,Intro_title))
        self.next_slide()

        slab = Rectangle(BLUE,height=3,width=5,fill_opacity=0.5,fill_color=BLUE)
        slab_lbl = Tex(r"Medium 2 ",font_size=35).move_to(1*UP+1.6*RIGHT)
        air_lbl = Tex(r"Medium 1 \\(Vacuum)",font_size=35).move_to(2.2*UP+1.6*RIGHT)
        air_lbl2 = Tex(r"Medium 1",font_size=35).move_to(2.2*UP+1.6*RIGHT)
        normal_1 = DashedLine(start=1.5*LEFT+2.5*UP,end=1.5*LEFT+0.5*UP,color=GREY_BROWN)
        i_ray = Ray(start=3*LEFT+3*UP,end=1.5*LEFT+1.5*UP,color=RED)
        r_ray = Ray(start=1.5*LEFT+1.5*UP,end=1.5*DOWN,color=RED)
        i_ang = Angle(normal_1,i_ray[0],radius=0.5,quadrant=(-1,-1),color=YELLOW)
        r_ang = Angle(normal_1,r_ray[0],radius=0.5,quadrant=(1,1),color=YELLOW)
        i_lbl = Tex(r"$\angle i$",font_size=30).next_to(i_ang,UP,buff=0.1)
        r_lbl = Tex(r"$\angle r$",font_size=30).next_to(r_ang,DOWN,buff=0.1)

        img = VGroup(slab,normal_1,i_ray,r_ray,slab_lbl,air_lbl,i_ang,r_ang,i_lbl,r_lbl,air_lbl2).next_to(Intro_title,RIGHT).to_corner(UR)
        self.add(img)
        self.play(FadeOut(air_lbl2))

        steps = ItemList(Item(r"Different medium have different abilities to bend or refract light. This bending ability of a medium is known as the refractive index.",pw="7.5 cm"),
                         Item(r"Types of Refractive index : \\",r"(1) Absolute refractive index $(n)$\\ \\", r" (2) Relative Refractive index $(n_{21})$ ",pw="7.5 cm"),
                         Item(r"(1) Absolute Refractive index : ", r"Absolute refractive index or simply \textbf{refractive index of Medium 2} $(n_2)$ is defined as ", r" the ratio of speed of light in vacuum $(c)$ (i.e., Medium 1) to the speed of light in the Medium 2 $(v_2)$",pw="13 cm"),
                         Item(r"n_2=\dfrac{\text{speed of light in vacuum}}{\text{speed of light in medium 2}}=\dfrac{c}{v_2}",math=True,dot=False),
                        buff=0.5).next_to(Intro_title,DOWN,buff=0.5).to_corner(LEFT,buff=0.2)

        steps[1][0].set_color(GOLD)
        steps[1][1].set_color(ORANGE)
        steps[1][2].set_color(YELLOW)
        steps[2][0].set_color(ORANGE)
        steps[2][2].set_color(YELLOW)
        sr = SurroundingRectangle(steps[3],color=RED)
        
        for item in steps:
            for subitem in item:
                self.play(Write(subitem))
                self.next_slide()
        self.play(Write(sr))

        self.next_slide()
        self.play(FadeOut(steps,air_lbl,sr),FadeIn(air_lbl2))

        steps2 = ItemList(Item(r"(2) Relative Refractive index : ", r"Relative refractive index of medium 2 with respect to medium 1 $(n_{21})$ is defined as ", r" the ratio of speed of light in medium 1 $(v_1)$  to the speed of light in the Medium 2 $(v_2)$",pw="7.5 cm"),
                         Item(r"n_{21}=\dfrac{\text{speed of light in medium 1}}{\text{speed of light in medium 2}}=\dfrac{v_1}{v_2}",r"=\dfrac{n_2}{n_1}=\dfrac{\sin(\angle i)}{\sin(\angle r)}",math=True,dot=False),
                        buff=1.5).next_to(Intro_title,DOWN,buff=1.5).to_corner(LEFT,buff=0.2)
        
        sr2 = SurroundingRectangle(steps2[1],color=RED)
        steps2[0][0].set_color(ORANGE)
        steps2[0][2].set_color(YELLOW)

        for item in steps2:
            for subitem in item:
                self.play(Write(subitem))
                self.next_slide()
        self.play(Write(sr2))
        self.next_slide()
        self.play(FadeOut(img,steps2,sr2))
        table = Table(
            [["Air", "1.0003", "Crown glass", "1.52"],
             ["Ice", "1.31" , "Canada Balsam", "1.53" ],
             ["Water", "1.33", "Rock salt", "1.54"],
             ["Alcohol", "1.36 " , "Carbon disulphide", "1.63"],
             ["Kerosene", "1.44", "Dense flint glass", "1.65"],
             ["Fused quartz", "1.46", "Ruby", "1.71"],
             ["Turpentine oil", "1.47", "Sapphire", "1.77"],
             ["Benzene", "1.50", "Diamond", "2.42"]],
            col_labels=[Text("Material\n Medium"), Text("Refractive \n Index"), Text("Material\n Medium"), Text("Refractive \n Index")],
            include_outer_lines=True,include_background_rectangle=True,background_rectangle_color=DARK_GREY).scale(0.44).next_to(Intro_title,DOWN).to_corner(LEFT,buff=2.5)
        
        table.get_col_labels().set_color(ORANGE)
        table_lbl = Tex("Table: Absolute refractive index of some material media",font_size=30).next_to(table,DOWN)
        
        self.play(Write(table.get_horizontal_lines()),Write(table.get_vertical_lines()))
        self.add(table,table_lbl)
        self.wait(2)
        self.next_slide()
        self.play(FadeOut(table,table_lbl))
        steps3 = ItemList(Item(r"Optical Density : ", r"The ability of a medium to refract light is also expressed in terms of its optical density.",pw="13 cm"),
                         Item(r"Optical density is not the same as mass density. ",pw="13 cm"),
                         Item(r"Denser Medium : ", r"In comparing two media, the one with the ", r"larger refractive index ", r"is optically denser medium than the other.",pw="13 cm"),
                         Item(r"Rarer Medium : ", r" The other medium of ", r"lower refractive index ", r"is optically rarer.",pw="13 cm"),
                         Item(r"The speed of light is higher in a rarer medium than a denser medium",pw="13 cm"),
                         Item(r"Thus, a ray of light traveling from a rarer medium to a denser medium slows down and bends \textbf{towards the normal}.",pw="13 cm",color=YELLOW_C),
                         Item(r"When it travels from a denser medium to a rarer medium, it speeds up and bends \textbf{away from the normal}.",pw="13 cm",color=YELLOW_C),
                        buff=0.35).next_to(Intro_title,DOWN,buff=0.5).to_corner(LEFT,buff=0.2)
        
        steps3[0][0].set_color(GOLD)
        steps3[2][0].set_color(GOLD)
        steps3[3][0].set_color(GOLD)
        steps3[2][2].set_color(PINK)
        steps3[3][2].set_color(PINK)

        for item in steps3:
            self.play(Write(item))
            self.next_slide()

        
class Lens(Slide):
    def construct(self):
        title = Title('CHAPTER 1 : LIGHT REFLECTION AND REFRACTION',color=GREEN,match_underline_width_to_text=True)
        self.add(title)
        Outline = Tex('Learning Objectives :',color=BLUE,font_size=35).next_to(title,DOWN).to_corner(LEFT,buff=0.1)
        self.add(Outline)
        list = BulletedList('Introduction',' Reflection And Laws of reflection','Spherical Mirrors','Image formation by Spherical Mirrors','Ray Diagrams','Uses of Concave and Convex Mirrors',
                            'Sign Convention','Mirror Formula and Magnification',font_size=35).next_to(Outline,DOWN).align_to(Outline,LEFT)

        list2 = BulletedList('Refraction of Light','Refraction through a Rectangular Glass Slab','Laws of Refraction','The Refractive Index',
                             'Refraction by Spherical Lenses',' Image Formation by Lenses \& Ray Diagrams',"Lens Formula \& Magnification","Power of a Lens",font_size=35).next_to(Outline,DOWN).next_to(list,RIGHT).align_to(list,UP)

        self.add(list,list2)
        self.next_slide(loop=True)
        self.play(FocusOn(list2[4]))
        self.play(Circumscribe(list2[4]))
        self.next_slide()
        self.play(RemoveTextLetterByLetter(list2))
        self.play(RemoveTextLetterByLetter(list))
        self.play(RemoveTextLetterByLetter(Outline))
        Intro_title = Title('Refraction by Spherical Lenses', color=GREEN,match_underline_width_to_text=True,underline_buff=0.15).to_corner(UL)
        self.play(ReplacementTransform(title,Intro_title))
        self.next_slide()
        steps = ItemList(Item(r"SPHERICAL LENS : ", r"A spherical lens is a transparent material bounded by two surfaces one or both of which are spherical.",pw="13 cm"),
                         Item(r" A lens is bound by at least one spherical surface. In such lenses, the other surface would be plane. Spherical lenses are of four main types",pw="13 cm"),
                        buff=0.35).next_to(Intro_title,DOWN,buff=0.5).to_corner(LEFT,buff=0.2)
        
        steps[0][0].set_color(GOLD)
        [l,pa,f,s1,s2] = ConvexLens(R=6.5)
        [l2,pa2,f2,s11,s22]= ConcaveLens(R=6.5,c2=False,pae=-0.45,pos=2.5)
        [pl,rect,sph] = PlanoConvexLens()
        [pl2,rect2,sph2] = PlanoConcaveLens()
        img = VGroup(l,l2,pl,pl2).arrange(RIGHT,buff=3).next_to(steps,DOWN)
        convex_lbl = Tex(r"Double Convex Lens \\(Or Convex Lens)",font_size=30).next_to(l,DOWN)
        concave_lbl = Tex(r"Double Concave Lens \\(Or Concave Lens)",font_size=30).next_to(l2,DOWN)
        plano_convex_lbl = Tex("Plano-Convex Lens",font_size=30).next_to(pl,DOWN)
        plano_concave_lbl = Tex("Plano-Concave Lens",font_size=30).next_to(pl2,DOWN)
        img.add(convex_lbl,concave_lbl,plano_convex_lbl,plano_concave_lbl)
        sr = SurroundingRectangle(img)

        steps2 = ItemList(Item(r"Convex lens : ", r"A double convex lens is bounded by two spherical surfaces, \textbf{curved outwards (bulging outwards)}.",pw="13 cm"),
                         Item(r"It is \textbf{thicker in the middle} and \textbf{thinner at the edges}.",pw="13 cm"),
                         Item(r"Convex lens converges light rays. So, it is also called \textbf{converging lenses}.",pw="13 cm"),
                        buff=0.35).next_to(Intro_title,DOWN,buff=0.5).to_corner(LEFT,buff=0.2)
        
        steps2[0][0].set_color(GOLD)

        steps3 = ItemList(Item(r"Concave lens : ", r"A double convex lens is bounded by two spherical surfaces, \textbf{curved inwards.}.",pw="13 cm"),
                         Item(r"It is \textbf{thinner in the middle} and \textbf{thicker at the edges}.",pw="13 cm"),
                         Item(r"Convex lens diverges light rays. So, it is also called \textbf{diverging lenses}.",pw="13 cm"),
                        buff=0.35).next_to(Intro_title,DOWN,buff=0.5).to_corner(LEFT,buff=0.2)
        
        steps3[0][0].set_color(GOLD)

        for item in steps:
            self.play(Write(item))
            self.next_slide()

        self.play(DrawBorderThenFill(img),Create(sr))
        self.next_slide()
        self.play(FadeOut(img,steps,sr))
        [l,pa,f,s1,s2] = ConvexLens(R=6.5,c2=False,pae=-0.45,pos=2.5)
        convex_lbl = Tex(r"Converging action of a convex lens.",font_size=35).next_to(l,DOWN)
        ir1 = Ray(start=l.get_center()+2.2*f*LEFT+0.5*UP,end=l.get_center()+0.5*UP,color=PURE_GREEN)
        ir2 = Ray(start=l.get_center()+2.2*f*LEFT-0.5*UP,end=l.get_center()-0.5*UP,color=PURE_GREEN)
        ir3 = Ray(start=l.get_center()+2.2*f*LEFT+1*UP,end=l.get_center()+1*UP,color=PURE_GREEN)
        ir4 = Ray(start=l.get_center()+2.2*f*LEFT-1*UP,end=l.get_center()-1*UP,color=PURE_GREEN)
        rr1 = Ray(start=ir1[0].get_end(),end=l.get_center()+f*RIGHT,color=PURE_GREEN,ext=0.2)
        rr2 = Ray(start=ir2[0].get_end(),end=l.get_center()+f*RIGHT,color=PURE_GREEN,ext=0.2)
        rr3 = Ray(start=ir3[0].get_end(),end=l.get_center()+f*RIGHT,color=PURE_GREEN,ext=0.2)
        rr4 = Ray(start=ir4[0].get_end(),end=l.get_center()+f*RIGHT,color=PURE_GREEN,ext=0.2)
        img2=VGroup(l,pa,convex_lbl,ir1,ir2,ir3,ir4,rr1,rr2,rr3,rr4).next_to(steps2,DOWN)
        sr2 = SurroundingRectangle(img2)
        self.play(DrawBorderThenFill(l),Write(convex_lbl))
        for item in steps2:
            for subitem in item:
                self.play(Write(subitem))
                self.next_slide()

        self.play(Create(VGroup(pa,ir1,ir2,ir3,ir4)))
        self.next_slide()
        self.play(Create(VGroup(rr1,rr2,rr3,rr4,sr2)))
        self.wait()

        self.next_slide()
        self.play(FadeOut(steps2,img2,sr2))
        [l2,pa2,f2,s11,s22]= ConcaveLens(R=6.5,c2=False,pae=-0.45)
        concave_lbl = Tex(r"Diverging action of a concave lens.",font_size=35).next_to(l2,DOWN)
        ir1 = Ray(start=l2.get_center()+2.2*f*LEFT+0.5*UP,end=l2.get_center()+0.5*UP,color=PURE_GREEN)
        ir2 = Ray(start=l2.get_center()+2.2*f*LEFT-0.5*UP,end=l2.get_center()-0.5*UP,color=PURE_GREEN)
        ir3 = Ray(start=l2.get_center()+2.2*f*LEFT+1*UP,end=l2.get_center()+1*UP,color=PURE_GREEN)
        ir4 = Ray(start=l2.get_center()+2.2*f*LEFT-1*UP,end=l2.get_center()-1*UP,color=PURE_GREEN)
        fr1 = DashedLine(start=l2.get_center()+f2*LEFT,end=ir1[0].get_end(),color=GREY)
        fr2 = DashedLine(start=l2.get_center()+f2*LEFT,end=ir2[0].get_end(),color=GREY)
        fr3 = DashedLine(start=l2.get_center()+f2*LEFT,end=ir3[0].get_end(),color=GREY)
        fr4 = DashedLine(start=l2.get_center()+f2*LEFT,end=ir4[0].get_end(),color=GREY)
        rr1 = Ray(start=fr1.get_end(),end=fr1.get_end()+2*fr1.get_unit_vector(),color=PURE_GREEN)
        rr2 = Ray(start=fr2.get_end(),end=fr2.get_end()+2*fr2.get_unit_vector(),color=PURE_GREEN)
        rr3 = Ray(start=fr3.get_end(),end=fr3.get_end()+2*fr3.get_unit_vector(),color=PURE_GREEN)
        rr4 = Ray(start=fr4.get_end(),end=fr4.get_end()+2*fr4.get_unit_vector(),color=PURE_GREEN)
        img3= VGroup(l2,concave_lbl,pa2,ir1,ir2,ir3,ir4,fr1,fr2,fr3,fr4,rr1,rr2,rr3,rr4).next_to(steps3,DOWN)
        sr3 = SurroundingRectangle(img3)

        self.play(DrawBorderThenFill(l2),Write(concave_lbl))
        for item in steps3:
            for subitem in item:
                self.play(Write(subitem))
                self.next_slide()
        
        self.play(Create(VGroup(pa2,ir1,ir2,ir3,ir4)))
        self.next_slide()
        self.play(Create(VGroup(rr1,rr2,rr3,rr4,fr1,fr2,fr3,fr4,sr3)))
        self.wait()

class LensTerms(Slide):
    def construct(self):
        title_lbl = Tex("Important Terms Related to Spherical Lenses:",font_size=40,color=GOLD)
        ul  = Underline(title_lbl,color=LIGHT_PINK)
        title = VGroup(title_lbl,ul).to_corner(UL)
        self.play(Write(title))
        centre = Item(r"(1) Centre of Curvature (C): ", r"The centres of the spheres that the spherical lens was a part of.", r" A spherical lens has two centres of curvatures ($C_1,\ C_2$).",pw="13 cm",dot=False).next_to(title,DOWN).align_to(title,LEFT)
        centre[0].set_color(YELLOW_C)
        self.next_slide()

        [l,pa,f,s1,s2] = ConvexLens(R=2.8,f1=False,f2=False,l=False,o=False)
        [l2,pa2,f2,s11,s22]= ConcaveLens(R=2.8,f1=False,f2=False,l=False,o=False)
        self.play(Create(VGroup(l,pa,s1,s2).next_to(centre,DOWN)),Write(centre[0]))
        self.wait()
        self.next_slide()
        self.play(FadeOut(VGroup(l,pa,s1,s2)))
        self.play(Create(VGroup(l2,pa2,s11,s22).next_to(centre,DOWN)))
        self.wait()
        self.next_slide()

        for item in centre[1:3]:
            self.play(Write(item))
            self.next_slide()
        
        p_axis = Item(r"(2) Principal Axis: ", r"An imaginary straight line passing through the two centres of curvature of a lens is called its principal axis.",pw="13 cm",dot=False).next_to(title,DOWN,buff=0.5).align_to(title,LEFT)
        p_axis[0].set_color(YELLOW_C)
        self.play(FadeOut(centre,VGroup(l2,pa2,s11,s22)))
        [l,pa,f,s1,s2] = ConvexLens(R=3,f1=False,f2=False)
        [l2,pa2,f2,s11,s22]= ConcaveLens(R=3,f1=False,f2=False)
        VGroup(VGroup(l,pa),VGroup(l2,pa2)).arrange(RIGHT).next_to(centre,DOWN,buff=3)
        pa_arrow = CurvedArrow(pa[0].get_start()+1.5*RIGHT,pa[0].get_start()+1.5*DOWN+2*RIGHT,tip_length=0.1,color=GREEN_C)
        pa2_arrow = CurvedArrow(pa2[0].get_start()+1.5*RIGHT,pa2[0].get_start()+1.5*DOWN+2*RIGHT,tip_length=0.1,color=GREEN_C)
        pa_lbl = Tex("Principal Axis", font_size=30,color=GREEN_C).move_to(pa_arrow.get_tip()).shift(0.2*DOWN)
        pa2_lbl = Tex("Principal Axis", font_size=30,color=GREEN_C).move_to(pa2_arrow.get_tip()).shift(0.2*DOWN)
        self.play(Write(p_axis[0]),Create(VGroup(l,pa[0:-1],pa_arrow,pa_lbl)),Create(VGroup(l2,pa2[0:-1],pa2_arrow,pa2_lbl)))
        self.wait()
        self.next_slide()
        self.play(Write(p_axis[1]))
        
        optical = Item(r"(3) Optical Centre (O): ", r" The central point of a lens is its optical centre.",r" A ray of light through the optical centre of a lens passes without suffering any deviation.",pw="13 cm",dot=False).next_to(p_axis,DOWN,buff=0.5).align_to(p_axis,LEFT)
        aperture = Item(r"(4) Aperture : ",r"The effective diameter of the circular outline of a spherical lens is called its aperture.",r" [Thin lenses $\rightarrow$ small aperture$(<R)$ and $OC_1=OC_2=R$]",pw="13 cm").next_to(optical,DOWN,buff=0.5).align_to(optical,LEFT)
        optical[0].set_color(YELLOW_C)
        aperture[0].set_color(YELLOW_C)
        aperture[2].set_color(ORANGE)
        ap_lbl = MyDoubLabArrow(label=Tex("Aperture",font_size=30,color=GOLD),start=l2.get_top(),end=l2.get_bottom(),tip_length=0.1,pos=0.2*RIGHT,color=GOLD).next_to(l2,RIGHT)

        self.play(Write(optical[0]))
        self.next_slide(loop=True)
        self.play(Create(VGroup(pa[-1],pa2[-1])))
        self.play(Wiggle(VGroup(pa[-1],pa2[-1])))
        self.next_slide()
        self.play(Write(optical[1]))
        self.next_slide()
        self.play(Write(optical[2]))
        self.next_slide()
        self.play(Write(aperture[0]),Write(ap_lbl))
        self.next_slide()
        self.play(Write(aperture[1]))
        self.next_slide()
        self.play(Write(aperture[2]))

        activity = Tex("Activity 10.11:",font_size=40,color=YELLOW_C).to_corner(UL,buff=0.1)
        img1 = ImageMobject("lensf4.png").to_corner(UR,buff=0).set_z_index(1)
        img2 = ImageMobject("lensf3.png").to_corner(UR,buff=0).set_z_index(2)
        img3 = ImageMobject("lensf2.png").to_corner(UR,buff=0).set_z_index(3)
        img4 = ImageMobject("lensf1.png").to_corner(UR,buff=0).set_z_index(4)
        procedure = ItemList(Item(r"Hold a convex lens in your hand.", r" Direct it towards the Sun.",pw="6 cm"),
                         Item(r" Focus the light from the Sun on a sheet of paper. Obtain a sharp bright image of the Sun.",pw="6 cm"),
                         Item(r"Hold the paper and the lens in the same position for a while. Keep observing the paper.",pw="6 cm"),
                         Item(r"We observe that the paper begins to burn producing smoke.",pw="6 cm"),
                         Item(r" Parallel sun rays were converged by the lens at the sharp bright spot formed on the paper.  The concentration of the sunlight at a point generated heat. This caused the paper to burn.",pw="6 cm"),
                        buff=0.35).next_to(activity,DOWN).to_corner(LEFT,buff=0.2)
        self.next_slide()
        self.play(FadeOut(p_axis,optical,aperture,VGroup(l,pa,pa_arrow,pa_lbl),VGroup(l2,pa2,pa2_arrow,pa2_lbl),ap_lbl,title))
        self.play(Write(activity))
        self.play(Write(procedure[0][0]),FadeIn(img1))
        self.next_slide()
        self.play(Write(procedure[0][1]),FadeIn(img2))
        self.next_slide()
        self.play(Write(procedure[1]))
        self.next_slide()
        self.play(Write(procedure[2]))
        self.next_slide()
        self.play(Write(procedure[3]))
        self.next_slide()
        self.play(FadeIn(img3),Write(procedure[4]))
        self.next_slide()
        self.play(FadeIn(img4))
        self.wait()
        
            
class Focus(Slide):
    def construct(self):
        steps3 = ItemList(Item(r"(5) Principal Focus of Convex Lens :", r" When several rays of light parallel to the principal axis are falling on a convex lens.", r" These rays, after refraction from the lens, are converging to a point on the principal axis.", r" This point on the principal axis is called the principal focus of the lens.",pw="6 cm"),
                         Item(r"(6) Principal Focus of Concave Lens :", r" When several rays of light parallel to the principal axis are falling on a convex lens.", r" These rays, after refraction from the lens, are appearing to diverge from a point on the principal axis.", r" This point on the principal axis is called the principal focus of the lens.",pw="6 cm"),
                         Item(r"(7) Focal Length (f) :", r" distance of the principal focus from the optical centre.",pw="13 cm"),
                           buff=0.35).to_corner(UL,buff=0.2)
        
        steps3[0][0].set_color(GOLD)
        steps3[1][0].set_color(GOLD)
        steps3[2][0].set_color(GOLD)
        [l,pa,f,s1,s2] = ConvexLens(R=6.5,c2=False,c1=False,pae=-0.45,pas=-0.45)
        ir1 = Ray(start=l.get_center()+1.2*f*LEFT+0.5*UP,end=l.get_center()+0.5*UP,color=PURE_GREEN)
        ir2 = Ray(start=l.get_center()+1.2*f*LEFT-0.5*UP,end=l.get_center()-0.5*UP,color=PURE_GREEN)
        ir3 = Ray(start=l.get_center()+1.2*f*LEFT+1*UP,end=l.get_center()+1*UP,color=PURE_GREEN)
        ir4 = Ray(start=l.get_center()+1.2*f*LEFT-1*UP,end=l.get_center()-1*UP,color=PURE_GREEN)
        rr1 = Ray(start=ir1[0].get_end(),end=l.get_center()+f*RIGHT,color=PURE_GREEN,ext=0.2)
        rr2 = Ray(start=ir2[0].get_end(),end=l.get_center()+f*RIGHT,color=PURE_GREEN,ext=0.2)
        rr3 = Ray(start=ir3[0].get_end(),end=l.get_center()+f*RIGHT,color=PURE_GREEN,ext=0.2)
        rr4 = Ray(start=ir4[0].get_end(),end=l.get_center()+f*RIGHT,color=PURE_GREEN,ext=0.2)
        fl1 = MyDoubLabArrow(label=Tex("f",font_size=35),start=l.get_center(),end=l.get_center()+f*RIGHT,tip_length=0.1,color=ORANGE,opacity=1).shift(1.5*DOWN)
        img2=VGroup(l,pa,ir1,ir2,ir3,ir4,rr1,rr2,rr3,rr4,fl1).next_to(steps3[0],RIGHT).align_to(steps3[0],UP)

        self.play(DrawBorderThenFill(l),Write(steps3[0][0]))
        self.next_slide()
        self.play(Create(VGroup(pa[0],pa[-1],ir1,ir2,ir3,ir4)),Write(steps3[0][1]))
        self.next_slide()
        self.play(Create(VGroup(rr1,rr2,rr3,rr4)),Write(steps3[0][2]))
        self.next_slide()
        self.play(Write(steps3[0][3]),Create(pa[2]),Create(pa[1]))
        self.wait()
        

        self.next_slide()
        [l2,pa2,f2,s11,s22]= ConcaveLens(R=6.5,c2=False,c1=False,pae=-0.45,pas=-0.45)
        ir1 = Ray(start=l2.get_center()+1.2*f*LEFT+0.5*UP,end=l2.get_center()+0.5*UP,color=PURE_GREEN)
        ir2 = Ray(start=l2.get_center()+1.2*f*LEFT-0.5*UP,end=l2.get_center()-0.5*UP,color=PURE_GREEN)
        ir3 = Ray(start=l2.get_center()+1.2*f*LEFT+1*UP,end=l2.get_center()+1*UP,color=PURE_GREEN)
        ir4 = Ray(start=l2.get_center()+1.2*f*LEFT-1*UP,end=l2.get_center()-1*UP,color=PURE_GREEN)
        fr1 = DashedLine(start=l2.get_center()+f2*LEFT,end=ir1[0].get_end(),color=GREY)
        fr2 = DashedLine(start=l2.get_center()+f2*LEFT,end=ir2[0].get_end(),color=GREY)
        fr3 = DashedLine(start=l2.get_center()+f2*LEFT,end=ir3[0].get_end(),color=GREY)
        fr4 = DashedLine(start=l2.get_center()+f2*LEFT,end=ir4[0].get_end(),color=GREY)
        rr1 = Ray(start=fr1.get_end(),end=fr1.get_end()+2*fr1.get_unit_vector(),color=PURE_GREEN)
        rr2 = Ray(start=fr2.get_end(),end=fr2.get_end()+2*fr2.get_unit_vector(),color=PURE_GREEN)
        rr3 = Ray(start=fr3.get_end(),end=fr3.get_end()+2*fr3.get_unit_vector(),color=PURE_GREEN)
        rr4 = Ray(start=fr4.get_end(),end=fr4.get_end()+2*fr4.get_unit_vector(),color=PURE_GREEN)
        fl2 = MyDoubLabArrow(label=Tex("f",font_size=35),start=l2.get_center(),end=l2.get_center()+f2*LEFT,tip_length=0.1,color=ORANGE,opacity=1).shift(1.5*DOWN)
        img3= VGroup(l2,pa2,ir1,ir2,ir3,ir4,fr1,fr2,fr3,fr4,rr1,rr2,rr3,rr4,fl2).next_to(img2,DOWN)

        
        self.play(DrawBorderThenFill(l2),Write(steps3[1][0]))
        self.next_slide()
        self.play(Create(VGroup(pa2[0],pa2[-1],ir1,ir2,ir3,ir4)),Write(steps3[1][1]))
        self.next_slide()
        self.play(Create(VGroup(rr1,rr2,rr3,rr4,fr1,fr2,fr3,fr4)),Write(steps3[1][2]))
        self.next_slide()
        self.play(Write(steps3[1][3]),Create(pa2[1]),Create(pa2[2]))
        self.next_slide()
        self.play(Write(steps3[2]),Create(fl1),Create(fl2))
        self.wait()


class ConvexRules(Slide):
    def construct(self):
        title = Title('CHAPTER 1 : LIGHT REFLECTION AND REFRACTION',color=GREEN,match_underline_width_to_text=True)
        self.add(title)
        Outline = Tex('Learning Objectives :',color=BLUE,font_size=35).next_to(title,DOWN).to_corner(LEFT,buff=0.1)
        self.add(Outline)
        list = BulletedList('Introduction',' Reflection And Laws of reflection','Spherical Mirrors','Image formation by Spherical Mirrors','Ray Diagrams','Uses of Concave and Convex Mirrors',
                            'Sign Convention','Mirror Formula and Magnification',font_size=35).next_to(Outline,DOWN).align_to(Outline,LEFT)

        list2 = BulletedList('Refraction of Light','Refraction through a Rectangular Glass Slab','Laws of Refraction','The Refractive Index',
                             'Refraction by Spherical Lenses',' Image Formation by Lenses \& Ray Diagrams',"Lens Formula \& Magnification","Power of a Lens",font_size=35).next_to(Outline,DOWN).next_to(list,RIGHT).align_to(list,UP)

        self.add(list,list2)
        self.next_slide(loop=True)
        self.play(FocusOn(list2[5]))
        self.play(Circumscribe(list2[5]))
        self.next_slide()
        self.play(RemoveTextLetterByLetter(list2))
        self.play(RemoveTextLetterByLetter(list))
        self.play(RemoveTextLetterByLetter(Outline))
        Intro_title = Title('Image Formation by Lenses and Ray Diagrams', color=GREEN,match_underline_width_to_text=True,underline_buff=0.15).to_corner(UL)
        self.play(ReplacementTransform(title,Intro_title))
        self.next_slide()
        Act = Tex("Activity 10.12 : Image formation by a convex lens for different positions of the object",font_size=35, color=GREEN,tex_environment="{minipage}{13cm}").next_to(Intro_title,DOWN).to_corner(LEFT,buff=0.2)
        self.play(Write(Act))

        t2 = MobjectTable(
            [[Text("At infinity"), Tex(r"At focus $F_2$",font_size=72), Text("Highly diminished,\n point-sized"), Text("Real and inverted")],
             [Tex(r"Beyond $C_1$ ($2F_1$)",font_size=72), Tex(r"Between $F_2$ and\\ $C_2 (2F_2)$",font_size=72), Text("Diminished"), Text("Real and inverted")],
             [Tex(r"At $C_1$ ($2F_1$)",font_size=72), Tex(r"At $C_2 (2F_2)$",font_size=72), Text("Same size"), Text("Real and inverted")],
            [Tex(r"Between $C_1$ ($2F_1$)\\ and $F_1$",font_size=72), Tex(r"Beyond $C_2$ ($2F_2$)",font_size=72), Text("Enlarged"), Text("Real and inverted")],
            [Tex(r"At $F_1$",font_size=72), Text("At infinity"), Text("Highly enlarged"), Text("Real and inverted")],
            [Tex(r"Between O and $F_1$",font_size=72), Text(" On the same side of\n the lens as the object"), Text("Enlarged"), Text("Virtual and erect")]],
            col_labels=[Text("Position of the\n Object"), Text("Position of the\n Image"),Text("Size of the\n Image"),Text("Nature of the\n Image")],
            row_labels=[Text("(1)"), Text("(2)"),Text("(3)"),Text("(4)"),Text("(5)"),Text("(6)")],
            include_outer_lines=True,).scale(0.4).next_to(Act,DOWN).to_corner(LEFT,buff=0.4)
        
        t2.get_col_labels().set_color(ORANGE)
        t2.get_row_labels().set_color(GOLD)
        
        self.play(Write(t2.get_horizontal_lines().set_color(BLUE_D)),Write(t2.get_vertical_lines().set_color(BLUE_D)))
        self.next_slide()

        for entry in t2.get_entries():
            self.play(Write(entry))
            self.next_slide()

        
        Act2 = Tex("Activity 10.13 : Image formation by a concave lens for different positions of the object",font_size=35, color=GREEN,tex_environment="{minipage}{13cm}").next_to(Intro_title,DOWN).to_corner(LEFT,buff=0.2)
        

        t1 = MobjectTable(
            [[Text("At infinity"), Tex(r"At focus $F_1$",font_size=72), Text("Highly diminished,\n point-sized"), Text("Virtual and erect")],
             [Tex(r"Between infinity and\\ optical centre O of\\ the lens",font_size=72), Tex(r"Between focus $F_1$ and\\ optical centre O",font_size=72), Text("Diminished"), Text("Virtual and erect")]],
            col_labels=[Text("Position of the\n Object"), Text("Position of the\n Image"),Text("Size of the\n Image"),Text("Nature of the\n Image")],
            row_labels=[Text("(1)"), Text("(2)")], include_outer_lines=True,).scale(0.4).next_to(Act2,DOWN).to_corner(LEFT,buff=0.4)
        
        t1.get_col_labels().set_color(ORANGE)
        t1.get_row_labels().set_color(GOLD)

        self.play(FadeOut(t2,Act))
        self.wait()
        self.play(Write(Act2))
        
        self.play(Write(t1.get_horizontal_lines().set_color(BLUE_D)),Write(t1.get_vertical_lines().set_color(BLUE_D)))
        self.next_slide()

        for entry in t1.get_entries():
            self.play(Write(entry))
            self.next_slide()
        
        Note = Tex("Note:  A concave lens will always give a virtual, erect and diminished image, irrespective of the position of the object.",font_size=35, color=RED,tex_environment="{minipage}{13cm}").next_to(t1,DOWN,buff=1).to_corner(LEFT,buff=0.2)
        self.play(Write(Note))
        self.wait()

class ConvexLensImg(Slide):
    def construct(self):
        title = Title('Ray Diagram for Convex Lens',color=GREEN,match_underline_width_to_text=True)
        self.play(Write(title))
        case1 = Tex(r"(1) A ray of light parallel to the principal axis of a convex lens,", r" passes through the principal focus on the other side of the lens.",font_size=45,color=GOLD_E,tex_environment="{minipage}{10cm}").next_to(title,DOWN).to_edge(LEFT)
        self.next_slide()
        [l,pa,f,s1,s2] = ConvexLens(R=6.5,pae=0,pas=0)
        ir1 = Ray(start=l.get_center()+2*f*LEFT+1.2*UP,end=l.get_center()+1.2*UP,color=PURE_GREEN)
        rr1 = Ray(start=ir1[0].get_end(),end=l.get_center()+f*RIGHT,color=PURE_GREEN,ext=0.4)
        img1=VGroup(l,pa,ir1,rr1).next_to(case1,DOWN,buff=1.5)

        anm = [case1[0],VGroup(l,pa,ir1),VGroup(rr1,case1[1])]

        for item in anm:
            self.play(Write(item))
            self.next_slide()

        self.play(FadeOut(case1,img1))
        case2 = Tex(r"(2) A ray of light passing through a principal focus,", r" after refraction from a convex lens, will emerge parallel to the principal axis. ",font_size=45,color=GOLD_E,tex_environment="{minipage}{10cm}").next_to(title,DOWN).to_edge(LEFT)
        self.next_slide()
        [l,pa,f,s1,s2] = ConvexLens(R=6.5,pae=0,pas=0)
        ir1 = Ray(start=l.get_center()+f*LEFT,end=l.get_center()-1.2*UP,color=PURE_GREEN,eext=0.7)
        rr1 = Ray(start=ir1[0].get_end(),end=ir1[0].get_end()+5*RIGHT,color=PURE_GREEN)
        img2=VGroup(l,pa,ir1,rr1).next_to(case2,DOWN,buff=1.5)

        anm = [case2[0],VGroup(l,pa,ir1),VGroup(rr1,case2[1])]

        for item in anm:
            self.play(Write(item))
            self.next_slide()

        self.play(FadeOut(case2,img2))

        case3 = Tex(r"(3)  A ray of light passing through the optical centre of a lens", r" will emerge without any deviation. ",font_size=45,color=GOLD_E,tex_environment="{minipage}{10cm}").next_to(title,DOWN).to_edge(LEFT)
        self.next_slide()
        [l,pa,f,s1,s2] = ConvexLens(R=6.5,pae=0,pas=0)
        ir1 = Ray(start=l.get_center()+f*LEFT+0.8*UP,end=l.get_center(),color=PURE_GREEN,eext=0.5)
        rr1 = Ray(start=ir1[0].get_end(),end=4*ir1[0].get_unit_vector(),color=PURE_GREEN)
        img3=VGroup(l,pa,ir1,rr1).next_to(case3,DOWN,buff=1.5)

        anm = [case3[0],VGroup(l,pa,ir1),VGroup(rr1,case3[1])]

        for item in anm:
            self.play(Write(item))
            self.next_slide()

        self.play(FadeOut(case3,img3,title))
        self.play(FadeIn(VGroup(img1,img2,img3).scale(0.8).arrange(DOWN)))
        self.next_slide()
        self.play(FadeOut(VGroup(img1,img2,img3)))


class ConvexImg(Slide):
    def construct(self):
        title = Title('Ray Diagram for Convex Lens',color=GREEN,match_underline_width_to_text=True)

        # 1st Ray Diagram
        pos= Tex(r"Position of Object (i): ", r"At infinity",font_size=35,color=YELLOW,tex_environment="{minipage}{13cm}").to_corner(UL,buff=0.1)
        pos[0].set_color(RED)
        self.play(Write(pos))
        self.next_slide()

        [l,pa,f,s1,s2] = ConvexLens(R=6.5,c2=False,pae=-0.4,pas=0.1)
        obj = Arrow(start=l.get_center()+2.8*f*LEFT,end=l.get_center()+2.8*f*LEFT+UP,color=RED,tip_length=0.2,buff=0)
        objlbl = Tex(r"Object",font_size=30).next_to(obj,DOWN)
        dline = DashedLine(start=l.get_center()+2.8*f*LEFT, end=l.get_center()+2*f*LEFT)
        ir1 = VGroup(DashedLine(start=l.get_center()+2.8*f*LEFT+UP, end=l.get_center()+2*f*LEFT+UP,color=PURE_GREEN), Ray(start=l.get_center()+2*f*LEFT+UP,end=l.get_center()+UP,color=PURE_GREEN))
        ir2 = VGroup(DashedLine(start=l.get_center()+2.8*f*LEFT-UP, end=l.get_center()+2*f*LEFT-UP,color=PURE_GREEN), Ray(start=l.get_center()+2*f*LEFT-UP,end=l.get_center()-UP,color=PURE_GREEN))
        rr1 = Ray(start=ir1[1][0].get_end(),end=l.get_center()+f*RIGHT,color=PURE_GREEN,ext=0.2)
        rr2 = Ray(start=ir2[1][0].get_end(),end=l.get_center()+f*RIGHT,color=PURE_GREEN,ext=0.2)
        imarrow = CurvedArrow(l.get_center()+f*RIGHT,l.get_center()+f*RIGHT+0.5*UP+0.5*RIGHT,color=ORANGE,tip_length=0.1)
        imlbl = Tex(r"Image",font_size=30).move_to(imarrow.get_tip()).shift(0.4*UP)
        img1=VGroup(l,obj,objlbl,dline,pa,ir1,ir2,rr1,rr2,imarrow,imlbl).next_to(title,DOWN,buff=0.5)

        anm1 = [VGroup(l,pa),VGroup(dline,obj,objlbl),ir1,rr1,ir2,rr2,VGroup(imarrow,imlbl)]
        t1 = MobjectTable(
            [[Tex(r"At the focus  ($F_2$)",font_size=72), Tex(r"Highly diminished, point-sized",font_size=72), Tex(r"Real and inverted",font_size=72)]],
            col_labels=[Text(r"Position of the Image"),Text("Size of the Image"),Text("Nature of the Image")],
            include_outer_lines=True,).scale(0.44).to_edge(DOWN).to_corner(LEFT,buff=0.8)
        
        t1.get_col_labels().set_color(ORANGE)

        for item in anm1:
            self.play(Write(item))
            self.wait(2)
            self.next_slide()

        self.play(Write(t1.get_horizontal_lines()),Write(t1.get_vertical_lines()))
        self.wait(2)
        self.next_slide()

        for j in range(3):
            for i in t1.get_columns()[j]:
                self.play(Write(i))
                self.next_slide()
        
        self.play(Unwrite(t1),Unwrite(img1),Unwrite(pos))
        self.wait(2)
        self.next_slide()


        # 2nd Ray Diagram
        pos= Tex(r"Position of Object (ii): ", r"Beyond $C_1 \ (2F_1)$",font_size=35,color=YELLOW,tex_environment="{minipage}{13cm}").to_corner(UL,buff=0.1)
        pos[0].set_color(RED)
        self.play(Write(pos))
        self.next_slide()

        [l,pa,f,s1,s2] = ConvexLens(R=6.5,pae=0.12,pas=0.1)
        obj = Arrow(start=l.get_center()+2.2*f*LEFT,end=l.get_center()+2.2*f*LEFT+UP,color=RED,tip_length=0.2,buff=0)
        objlbl = Tex(r"Object",font_size=30).next_to(obj,RIGHT)
        ir1 = Ray(start=l.get_center()+2.2*f*LEFT+UP,end=l.get_center()+UP,color=PURE_GREEN)
        ir2 = Ray(start=l.get_center()+2.2*f*LEFT+UP,end=l.get_center(),color=PURE_GREEN)
        rr1 = Ray(start=ir1[0].get_end(),end=l.get_center()+f*RIGHT,color=PURE_GREEN,ext=1.1)
        rr2 = Ray(start=ir2[0].get_end(),end=4*ir2[0].get_unit_vector(),color=PURE_GREEN,ext=0.7)
        img_pos = Myintersection(rr2[0],rr1[0])[0]
        imarrow = Arrow(start=[img_pos[0],0,0],end=img_pos,color=RED,tip_length=0.2,buff=0)
        imlbl = Tex(r"Image",font_size=30).next_to(imarrow,UP)
        img1=VGroup(l,obj,objlbl,pa,ir1,ir2,rr1,rr2,imarrow,imlbl).next_to(title,DOWN,buff=0.5)

        anm1 = [VGroup(l,pa),VGroup(obj,objlbl),ir1,rr1,ir2,rr2,VGroup(imarrow,imlbl)]

        t1 = MobjectTable(
            [[Tex("Between $F_2$ and $C_2 (2F_2)$",font_size=72), Tex("Diminished",font_size=72), Tex("Real and inverted",font_size=72)]],
            col_labels=[Text("Position of the Image"),Text("Size of the Image"),Text("Nature of the Image")],
            include_outer_lines=True,).scale(0.44).to_edge(DOWN).to_corner(LEFT,buff=0.8)
        
        t1.get_col_labels().set_color(ORANGE)

        for item in anm1:
            self.play(Write(item))
            self.wait(2)
            self.next_slide()

        self.play(Write(t1.get_horizontal_lines()),Write(t1.get_vertical_lines()))
        self.wait(2)
        self.next_slide()

        for j in range(3):
            for i in t1.get_columns()[j]:
                self.play(Write(i))
                self.next_slide()
        
        self.play(Unwrite(t1),Unwrite(img1),Unwrite(pos))
        self.wait(2)
        self.next_slide()

        # 3rd Ray Diagram
        pos= Tex(r"Position of Object (iii): ", r"At $C_1 \ (2F_1)$",font_size=35,color=YELLOW,tex_environment="{minipage}{13cm}").to_corner(UL,buff=0.1)
        pos[0].set_color(RED)
        self.play(Write(pos))
        self.next_slide()

        [l,pa,f,s1,s2] = ConvexLens(R=6.5,pae=0.05,pas=0.05)
        obj = Arrow(start=l.get_center()+2*f*LEFT,end=l.get_center()+2*f*LEFT+UP,color=RED,tip_length=0.2,buff=0)
        objlbl = Tex(r"Object",font_size=30).next_to(obj,RIGHT)
        ir1 = Ray(start=l.get_center()+2*f*LEFT+UP,end=l.get_center()+UP,color=PURE_GREEN)
        ir2 = Ray(start=l.get_center()+2*f*LEFT+UP,end=l.get_center(),color=PURE_GREEN)
        rr1 = Ray(start=ir1[0].get_end(),end=l.get_center()+f*RIGHT,color=PURE_GREEN,ext=1.1,pos=0.3)
        rr2 = Ray(start=ir2[0].get_end(),end=4*ir2[0].get_unit_vector(),color=PURE_GREEN,ext=0.7)
        img_pos = Myintersection(rr2[0],rr1[0])[0]
        imarrow = Arrow(start=[img_pos[0],0,0],end=img_pos,color=RED,tip_length=0.2,buff=0)
        imlbl = Tex(r"Image",font_size=30).next_to(imarrow,RIGHT)
        img1=VGroup(l,obj,objlbl,pa,ir1,ir2,rr1,rr2,imarrow,imlbl).next_to(title,DOWN,buff=0.5)

        anm1 = [VGroup(l,pa),VGroup(obj,objlbl),ir1,rr1,ir2,rr2,VGroup(imarrow,imlbl)]

        t1 = MobjectTable(
            [[Tex("At $C_2 (2F_2)$",font_size=72), Tex("Same Size",font_size=72), Tex("Real and inverted",font_size=72)]],
            col_labels=[Text("Position of the Image"),Text("Size of the Image"),Text("Nature of the Image")],
            include_outer_lines=True,).scale(0.44).to_edge(DOWN).to_corner(LEFT,buff=0.8)
        
        t1.get_col_labels().set_color(ORANGE)

        for item in anm1:
            self.play(Write(item))
            self.wait(2)
            self.next_slide()

        self.play(Write(t1.get_horizontal_lines()),Write(t1.get_vertical_lines()))
        self.wait(2)
        self.next_slide()

        for j in range(3):
            for i in t1.get_columns()[j]:
                self.play(Write(i))
                self.next_slide()
        
        self.play(Unwrite(t1),Unwrite(img1),Unwrite(pos))
        self.wait(2)
        self.next_slide()


        # 4th Ray Diagram
        pos= Tex(r"Position of Object (iv): ", r"Between $C_1$ and  $F_1$",font_size=35,color=YELLOW,tex_environment="{minipage}{13cm}").to_corner(UL,buff=0.1)
        pos[0].set_color(RED)
        self.play(Write(pos))
        self.next_slide()

        [l,pa,f,s1,s2] = ConvexLens(R=5.5,pae=0.51,pas=0.05)
        obj = Arrow(start=l.get_center()+1.5*f*LEFT,end=l.get_center()+1.5*f*LEFT+UP,color=RED,tip_length=0.2,buff=0)
        objlbl = Tex(r"Object",font_size=30).next_to(obj,RIGHT)
        ir1 = Ray(start=l.get_center()+1.5*f*LEFT+UP,end=l.get_center()+UP,color=PURE_GREEN)
        ir2 = Ray(start=l.get_center()+1.5*f*LEFT+UP,end=l.get_center(),color=PURE_GREEN)
        rr1 = Ray(start=ir1[0].get_end(),end=l.get_center()+f*RIGHT,color=PURE_GREEN,ext=2.1)
        rr2 = Ray(start=ir2[0].get_end(),end=6*ir2[0].get_unit_vector(),color=PURE_GREEN,ext=0.45)
        img_pos = Myintersection(rr2[0],rr1[0])[0]
        imarrow = Arrow(start=[img_pos[0],0,0],end=img_pos,color=RED,tip_length=0.2,buff=0)
        imlbl = Tex(r"Image",font_size=30).next_to(imarrow,LEFT)
        img1=VGroup(l,obj,objlbl,pa,ir1,ir2,rr1,rr2,imarrow,imlbl).next_to(title,DOWN,buff=0.5)

        anm1 = [VGroup(l,pa),VGroup(obj,objlbl),ir1,rr1,ir2,rr2,VGroup(imarrow,imlbl)]

        t1 = MobjectTable(
            [[Tex(r"Beyond $C_2$ ($2F_2$)",font_size=72), Tex(r"Enlarged",font_size=72), Tex(r"Real and inverted",font_size=72)]],
            col_labels=[Text(r"Position of the Image"),Text("Size of the Image"),Text("Nature of the Image")],
            include_outer_lines=True,).scale(0.44).to_edge(DOWN).to_corner(LEFT,buff=0.8)
        
        t1.get_col_labels().set_color(ORANGE)

        for item in anm1:
            self.play(Write(item))
            self.wait(2)
            self.next_slide()

        self.play(Write(t1.get_horizontal_lines()),Write(t1.get_vertical_lines()))
        self.wait(2)
        self.next_slide()

        for j in range(3):
            for i in t1.get_columns()[j]:
                self.play(Write(i))
                self.next_slide()
        
        self.play(Unwrite(t1),Unwrite(img1),Unwrite(pos))
        self.wait(2)
        self.next_slide()

        # 5th Ray Diagram
        pos= Tex(r"Position of Object (v): ", r"At  $F_1$",font_size=35,color=YELLOW,tex_environment="{minipage}{13cm}").to_corner(UL,buff=0.1)
        pos[0].set_color(RED)
        self.play(Write(pos))
        self.next_slide()

        [l,pa,f,s1,s2] = ConvexLens(R=5.5,pae=0.45,pas=0.05)
        obj = Arrow(start=l.get_center()+1*f*LEFT,end=l.get_center()+1*f*LEFT+UP,color=RED,tip_length=0.2,buff=0)
        objlbl = Tex(r"Object",font_size=30).next_to(obj,RIGHT)
        ir1 = Ray(start=l.get_center()+1*f*LEFT+UP,end=l.get_center()+UP,color=PURE_GREEN)
        ir2 = Ray(start=l.get_center()+1*f*LEFT+UP,end=l.get_center(),color=PURE_GREEN)
        rr1 = Ray(start=ir1[0].get_end(),end=l.get_center()+f*RIGHT,color=PURE_GREEN,ext=1.8)
        rr2 = Ray(start=ir2[0].get_end(),end=4*ir2[0].get_unit_vector(),color=PURE_GREEN,ext=0.65)
        imlbl = Tex(r"At $\infty$",font_size=30).move_to(rr2[0].get_end()).shift(0.4*UP)
        img1=VGroup(l,obj,objlbl,pa,ir1,ir2,rr1,rr2,imlbl).next_to(title,DOWN,buff=0.5)

        anm1 = [VGroup(l,pa),VGroup(obj,objlbl),ir1,rr1,ir2,rr2,imlbl]

        t1 = MobjectTable(
            [[Tex(r"At infinity $(\infty)$",font_size=72), Tex(r"Highly Magnified \\ (Highly Enlarged)",font_size=72), Tex(r"Real and inverted",font_size=72)]],
            col_labels=[Text(r"Position of the Image"),Text("Size of the Image"),Text("Nature of the Image")],
            include_outer_lines=True,).scale(0.44).to_edge(DOWN).to_corner(LEFT,buff=0.8)
        
        t1.get_col_labels().set_color(ORANGE)

        for item in anm1:
            self.play(Write(item))
            self.wait(2)
            self.next_slide()

        self.play(Write(t1.get_horizontal_lines()),Write(t1.get_vertical_lines()))
        self.wait(2)
        self.next_slide()

        for j in range(3):
            for i in t1.get_columns()[j]:
                self.play(Write(i))
                self.next_slide()
        
        self.play(Unwrite(t1),Unwrite(img1),Unwrite(pos))
        self.wait(2)
        self.next_slide()

        # 6th Ray Diagram
        pos= Tex(r"Position of Object (vi): ", r"Between  $F_1$ and $O$",font_size=35,color=YELLOW,tex_environment="{minipage}{13cm}").to_corner(UL,buff=0.1)
        pos[0].set_color(RED)
        self.play(Write(pos))
        self.next_slide()

        [l,pa,f,s1,s2] = ConvexLens(R=5.5,pae=-0.3,pas=0.6,c2=False)
        obj = Arrow(start=l.get_center()+0.75*f*LEFT,end=l.get_center()+0.75*f*LEFT+UP,color=RED,tip_length=0.2,buff=0)
        objlbl = Tex(r"Object",font_size=30).next_to(obj,LEFT)
        ir1 = Ray(start=l.get_center()+0.75*f*LEFT+UP,end=l.get_center()+UP,color=PURE_GREEN)
        ir2 = Ray(start=l.get_center()+0.75*f*LEFT+UP,end=l.get_center(),color=PURE_GREEN)
        rr1 = Ray(start=ir1[0].get_end(),end=l.get_center()+f*RIGHT,color=PURE_GREEN,ext=1)
        rr2 = Ray(start=ir2[0].get_end(),end=3.5*ir2[0].get_unit_vector(),color=PURE_GREEN,ext=0.2)
        er1 = DashedLine(start = rr1[0].get_start(),end= rr1[0].get_start()-9.5*rr1[0].get_unit_vector(),color=GREY)
        er2 = DashedLine(start = rr2[0].get_start(),end= rr2[0].get_start()-9.5*rr2[0].get_unit_vector(),color=GREY)
        imlbl = Tex(r"At $\infty$",font_size=30).next_to(rr2,UR)
        img_pos = Myintersection(er2,er1)[0]
        imarrow = Arrow(start=[img_pos[0],0,0],end=img_pos,color=RED,tip_length=0.2,buff=0)
        imlbl = Tex(r"Image",font_size=30).next_to(imarrow,RIGHT)
        img1=VGroup(l,obj,objlbl,pa,ir1,ir2,rr1,rr2,er1,er2,imarrow,imlbl).next_to(title,DOWN,buff=0.5)

        anm1 = [VGroup(l,pa),VGroup(obj,objlbl),ir1,rr1,ir2,rr2,VGroup(er1,er2),VGroup(imarrow,imlbl)]

        t1 = MobjectTable(
            [[Tex(r"On the same side of\\ the lens as the object",font_size=72), Tex(r"Enlarged",font_size=72), Tex(r"Virtual and Erect",font_size=72)]],
            col_labels=[Text(r"Position of the Image"),Text("Size of the Image"),Text("Nature of the Image")],
            include_outer_lines=True,).scale(0.44).next_to(title,DOWN,buff=0.2).to_edge(RIGHT)
        
        t1.get_col_labels().set_color(ORANGE)

        for item in anm1:
            self.play(Write(item))
            self.wait(2)
            self.next_slide()

        self.play(Write(t1.get_horizontal_lines()),Write(t1.get_vertical_lines()))
        self.wait(2)
        self.next_slide()

        for j in range(3):
            for i in t1.get_columns()[j]:
                self.play(Write(i))
                self.next_slide()
        
        self.play(Unwrite(t1),Unwrite(img1),Unwrite(pos))
        self.wait(2)
        self.next_slide()
class ConcaveLensImg(Slide):
    def construct(self):
        title = Title('Ray Diagram for Concave Lens',color=GREEN,match_underline_width_to_text=True)
        self.play(Write(title))
        case1 = Tex(r"(1) A ray of light parallel to the principal axis of a concave lens,", r"after refraction the ray appears to diverge from the principal focus located on the same side of the lens. ",font_size=45,color=GOLD_E,tex_environment="{minipage}{10cm}").next_to(title,DOWN).to_edge(LEFT)
        self.next_slide()
        [l,pa,f,s1,s2] = ConcaveLens(R=6.5,pae=0,pas=0)
        ir1 = Ray(start=l.get_center()+2*f*LEFT+1.2*UP,end=l.get_center()+1.2*UP,color=PURE_GREEN)
        drr = DashedLine(start=l.get_center()+f*LEFT,end= ir1[0].get_end(),color=GREY_A)
        rr1 = Ray(start=ir1[0].get_end(),end=ir1[0].get_end()+3*drr.get_unit_vector(),color=PURE_GREEN,ext=0.4)
        img1=VGroup(l,pa,ir1,rr1,drr).next_to(case1,DOWN,buff=0.1)

        anm = [case1[0],VGroup(l,pa,ir1),VGroup(rr1,drr,case1[1])]

        for item in anm:
            self.play(Write(item))
            self.next_slide()

        self.play(FadeOut(case1,img1))
        case2 = Tex(r"(2) A ray of light appearing to meet at the principal focus of a concave lens,", r" after refraction from a concave lens, will emerge parallel to the principal axis. ",font_size=45,color=GOLD_E,tex_environment="{minipage}{10cm}").next_to(title,DOWN).to_edge(LEFT)
        self.next_slide()
        [l,pa,f,s1,s2] = ConcaveLens(R=6.5,pae=0,pas=0)
        rr1 = Ray(start=l.get_center()-1.2*UP,end=l.get_center()+1.5*f*RIGHT-1.2*UP,color=PURE_GREEN)
        drr = DashedLine(start=l.get_center()-1.2*UP,end=l.get_center()+f*RIGHT,color=GREY_A)
        ir1 = Ray(start=l.get_center()-1.2*UP-3*drr.get_unit_vector(),end=l.get_center()-1.2*UP,color=PURE_GREEN)
        
        img2=VGroup(l,pa,ir1,rr1,drr).next_to(case2,DOWN,buff=1)

        anm = [case2[0],VGroup(l,pa,ir1,drr),VGroup(rr1,case2[1])]

        for item in anm:
            self.play(Write(item))
            self.next_slide()

        self.play(FadeOut(case2,img2))

        case3 = Tex(r"(3)  A ray of light passing through the optical centre of a lens", r" will emerge without any deviation. ",font_size=45,color=GOLD_E,tex_environment="{minipage}{10cm}").next_to(title,DOWN).to_edge(LEFT)
        self.next_slide()
        [l,pa,f,s1,s2] = ConcaveLens(R=6.5,pae=0,pas=0)
        ir1 = Ray(start=l.get_center()+f*LEFT+0.8*UP,end=l.get_center(),color=PURE_GREEN,eext=0.5)
        rr1 = Ray(start=ir1[0].get_end(),end=4*ir1[0].get_unit_vector(),color=PURE_GREEN)
        img3=VGroup(l,pa,ir1,rr1).next_to(case3,DOWN,buff=1)

        anm = [case3[0],VGroup(l,pa,ir1),VGroup(rr1,case3[1])]

        for item in anm:
            self.play(Write(item))
            self.next_slide()

        self.play(FadeOut(case3,img3,title))
        self.play(FadeIn(VGroup(img1,img2,img3).scale(0.65).arrange(DOWN)))
        self.next_slide()
        self.play(FadeOut(VGroup(img1,img2,img3)))


class ConcaveImg(Slide):
    def construct(self):
        title = Title('Ray Diagram for Concave Lens',color=GREEN,match_underline_width_to_text=True)

        # 1st Ray Diagram
        pos= Tex(r"Position of Object (i): ", r"At infinity",font_size=35,color=YELLOW,tex_environment="{minipage}{13cm}").to_corner(UL,buff=0.1)
        pos[0].set_color(RED)
        self.play(Write(pos))
        self.next_slide()

        [l,pa,f,s1,s2] = ConcaveLens(R=6.5,c2=False,pae=-0.4,pas=0.1)
        obj = Arrow(start=l.get_center()+2.8*f*LEFT,end=l.get_center()+2.8*f*LEFT+UP,color=RED,tip_length=0.2,buff=0)
        objlbl = Tex(r"Object",font_size=30).next_to(obj,DOWN)
        dline = DashedLine(start=l.get_center()+2.8*f*LEFT, end=l.get_center()+2*f*LEFT)
        ir1 = VGroup(DashedLine(start=l.get_center()+2.8*f*LEFT+UP, end=l.get_center()+2*f*LEFT+UP,color=PURE_GREEN), Ray(start=l.get_center()+2*f*LEFT+UP,end=l.get_center()+UP,color=PURE_GREEN))
        ir2 = VGroup(DashedLine(start=l.get_center()+2.8*f*LEFT-UP, end=l.get_center()+2*f*LEFT-UP,color=PURE_GREEN), Ray(start=l.get_center()+2*f*LEFT-UP,end=l.get_center()-UP,color=PURE_GREEN))
        dr1 = DashedLine(start=ir1[1][0].get_end(),end=l.get_center()+f*LEFT,color=GREY_A)
        dr2 = DashedLine(start=ir2[1][0].get_end(),end=l.get_center()+f*LEFT,color=GREY_A)
        rr1 = Ray(start=ir1[1][0].get_end(),end=ir1[1][0].get_end()-2*dr1.get_unit_vector(),color=PURE_GREEN,ext=0.2)
        rr2 = Ray(start=ir2[1][0].get_end(),end=ir2[1][0].get_end()-2*dr2.get_unit_vector(),color=PURE_GREEN,ext=0.2)
        imarrow = CurvedArrow(l.get_center()+f*LEFT,l.get_center()+f*LEFT+0.5*UP+0.5*LEFT,color=ORANGE,tip_length=0.1)
        imlbl = Tex(r"Image",font_size=30).move_to(imarrow.get_tip()).shift(0.1*UP)
        img1=VGroup(l,obj,objlbl,dline,pa,ir1,ir2,rr1,rr2,dr1,dr2,imarrow,imlbl).next_to(title,DOWN,buff=0.5)

        anm1 = [VGroup(l,pa),VGroup(dline,obj,objlbl),ir1,VGroup(rr1,dr1),ir2,VGroup(rr2,dr2),VGroup(imarrow,imlbl)]
        t1 = MobjectTable(
            [[Tex(r"At the focus  ($F_1$)",font_size=72), Tex(r"Highly diminished, point-sized",font_size=72), Tex(r"Virtual and Erect",font_size=72)]],
            col_labels=[Text(r"Position of the Image"),Text("Size of the Image"),Text("Nature of the Image")],
            include_outer_lines=True,).scale(0.44).to_edge(DOWN).to_corner(LEFT,buff=0.8)
        
        t1.get_col_labels().set_color(ORANGE)

        for item in anm1:
            self.play(Write(item))
            self.wait(2)
            self.next_slide()

        self.play(Write(t1.get_horizontal_lines()),Write(t1.get_vertical_lines()))
        self.wait(2)
        self.next_slide()

        for j in range(3):
            for i in t1.get_columns()[j]:
                self.play(Write(i))
                self.next_slide()
        
        self.play(Unwrite(t1),Unwrite(img1),Unwrite(pos))
        self.wait(2)
        self.next_slide()

        # 2nd Ray Diagram
        pos= Tex(r"Position of Object (ii): ", r"Between infinity and optical centre O of the lens",font_size=35,color=YELLOW,tex_environment="{minipage}{13cm}").to_corner(UL,buff=0.1)
        pos[0].set_color(RED)
        self.play(Write(pos))
        self.next_slide()

        [l,pa,f,s1,s2] = ConcaveLens(R=6.5,c2=False,pae=-0.4,pas=0.1)
        obj = Arrow(start=l.get_center()+1.5*f*LEFT,end=l.get_center()+1.5*f*LEFT+UP,color=RED,tip_length=0.2,buff=0)
        objlbl = Tex(r"Object",font_size=30).next_to(obj,DOWN)
        ir1 = Ray(start=l.get_center()+1.5*f*LEFT+UP,end=l.get_center()+UP,color=PURE_GREEN)
        ir2 = Ray(start=l.get_center()+1.5*f*LEFT+UP,end=l.get_center(),color=PURE_GREEN)
        dr1 = DashedLine(start=ir1[0].get_end(),end=l.get_center()+f*LEFT,color=GREY_A)
        rr1 = Ray(start=ir1[0].get_end(),end=ir1[0].get_end()-2*dr1.get_unit_vector(),color=PURE_GREEN,ext=0.3)
        rr2 = Ray(start=ir2[0].get_end(),end=3*ir2[0].get_unit_vector(),color=PURE_GREEN,ext=0.1)
        img_pos = Myintersection(dr1,ir2[0])[0]
        imarrow = Arrow(start=[img_pos[0],0,0],end=img_pos,color=RED,tip_length=0.2,buff=0)
        imlbl = Tex(r"Image",font_size=30).next_to(imarrow,DOWN)
        img1=VGroup(l,obj,objlbl,dline,pa,ir1,ir2,rr1,rr2,dr1,imarrow,imlbl).next_to(title,DOWN,buff=0.5)

        anm1 = [VGroup(l,pa),VGroup(obj,objlbl),ir1,VGroup(rr1,dr1),ir2,rr2,VGroup(imarrow,imlbl)]
        t1 = MobjectTable(
            [[Tex(r"Between focus ($F_1$) and optical centre O ",font_size=72), Tex(r"Diminished",font_size=72), Tex(r"Virtual and Erect",font_size=72)]],
            col_labels=[Text(r"Position of the Image"),Text("Size of the Image"),Text("Nature of the Image")],
            include_outer_lines=True,).scale(0.44).to_edge(DOWN).to_corner(LEFT,buff=0.8)
        
        t1.get_col_labels().set_color(ORANGE)

        for item in anm1:
            self.play(Write(item))
            self.wait(2)
            self.next_slide()

        self.play(Write(t1.get_horizontal_lines()),Write(t1.get_vertical_lines()))
        self.wait(2)
        self.next_slide()

        for j in range(3):
            for i in t1.get_columns()[j]:
                self.play(Write(i))
                self.next_slide()
        
        self.play(Unwrite(t1),FadeOut(img1),Unwrite(pos))
        self.wait(2)
        self.next_slide()

        sign = Tex(r"Sign convention for spherical lenses : ",font_size=40,color=YELLOW,tex_environment="{minipage}{13cm}").to_corner(UL,buff=0.1)

        steps3 = ItemList(Item(r" For lenses, sign convention are similar to the one used for spherical mirrors. Except that all measurements are taken from the optical centre (O) of the lens.",pw="13 cm"),
                         Item(r"Focal length of Convex lens is Positive",pw="6 cm"),
                         Item(r"Focal length of Concave lens is negative",pw="6 cm"),
                           buff=0.4).next_to(sign,DOWN).to_edge(LEFT,buff=0.2)
        
        [l,pa,f,s1,s2] = ConvexLens(R=5.5,pae=0.51,pas=0.05)
        obj = Arrow(start=l.get_center()+1.5*f*LEFT,end=l.get_center()+1.5*f*LEFT+UP,color=RED,tip_length=0.2,buff=0)
        objlbl = Tex(r"Object",font_size=30).next_to(obj,RIGHT)
        ir1 = Ray(start=l.get_center()+1.5*f*LEFT+UP,end=l.get_center()+UP,color=PURE_GREEN)
        ir2 = Ray(start=l.get_center()+1.5*f*LEFT+UP,end=l.get_center(),color=PURE_GREEN)
        rr1 = Ray(start=ir1[0].get_end(),end=l.get_center()+f*RIGHT,color=PURE_GREEN,ext=2.1)
        rr2 = Ray(start=ir2[0].get_end(),end=6*ir2[0].get_unit_vector(),color=PURE_GREEN,ext=0.45)
        img_pos = Myintersection(rr2[0],rr1[0])[0]
        imarrow = Arrow(start=[img_pos[0],0,0],end=img_pos,color=RED,tip_length=0.2,buff=0)
        imlbl = Tex(r"Image",font_size=30).next_to(imarrow,LEFT)
        img2=VGroup(l,obj,objlbl,pa,ir1,ir2,rr1,rr2,imarrow,imlbl).next_to(title,DOWN,buff=0.5)
        img3= VGroup(img2,img1).arrange(LEFT).scale(0.55).next_to(steps3,DOWN)
        
        self.play(Write(sign),FadeIn(img3))
        self.next_slide()
        for item in steps3:
            self.play(Write(item))
            self.next_slide()


class LensFormula(Slide):
    def construct(self):
        title = Title('CHAPTER 1 : LIGHT REFLECTION AND REFRACTION',color=GREEN,match_underline_width_to_text=True)
        self.add(title)
        Outline = Tex('Learning Objectives :',color=BLUE,font_size=35).next_to(title,DOWN).to_corner(LEFT,buff=0.1)
        self.add(Outline)
        list = BulletedList('Introduction',' Reflection And Laws of reflection','Spherical Mirrors','Image formation by Spherical Mirrors','Ray Diagrams','Uses of Concave and Convex Mirrors',
                            'Sign Convention','Mirror Formula and Magnification',font_size=35).next_to(Outline,DOWN).align_to(Outline,LEFT)

        list2 = BulletedList('Refraction of Light','Refraction through a Rectangular Glass Slab','Laws of Refraction','The Refractive Index',
                             'Refraction by Spherical Lenses',' Image Formation by Lenses \& Ray Diagrams',"Lens Formula \& Magnification","Power of a Lens",font_size=35).next_to(Outline,DOWN).next_to(list,RIGHT).align_to(list,UP)

        self.add(list,list2)
        self.next_slide(loop=True)
        self.play(FocusOn(list2[6]))
        self.play(Circumscribe(list2[6]))
        self.next_slide()
        self.play(RemoveTextLetterByLetter(list2))
        self.play(RemoveTextLetterByLetter(list))
        self.play(RemoveTextLetterByLetter(Outline))
        Intro_title = Title('Lens Formula and Magnification', color=GREEN,match_underline_width_to_text=True,underline_buff=0.15).to_corner(UL)
        self.play(ReplacementTransform(title,Intro_title))
        self.next_slide()
        steps = ItemList(Item(r"Lens Formula: ",r" For spherical lenses, the relationship between $u$, $v$ and $f$ is given by lens formula.",pw="13 cm"),
                         Item(r"$\dfrac{1}{f}=\dfrac{1}{v}-\dfrac{1}{u}$",pw="13 cm"),
                         Item(r"Magnification $(m)$ : ", r" It is the ratio of height of image $(h_i)$ to the height of the object $(h_o)$",pw="13 cm"),
                         Item(r"$m = \dfrac{h_i}{h_o}$",pw="13 cm"),
                         Item(r"For spherical lenses the magnification $m$ is also related to the object distance $(u)$ and image distance $(v)$. ",pw="13 cm"),
                         Item( r"$m =\dfrac{h_i}{h_o}= \dfrac{v}{u}$",pw="13 cm"),
                        buff=MED_SMALL_BUFF).next_to(Intro_title,DOWN,buff=0.15).to_corner(LEFT,buff=0.1)
        
        sr1 = SurroundingRectangle(steps[1])
        sr2 = SurroundingRectangle(steps[5])
        self.add(steps)
        
        self.play(Write(sr1),Write(sr2))
        self.wait()


class Ex18(Slide):
    def construct(self):
        ex_title = Tex(r"Example 18 :", r" A concave lens has focal length of 15 cm. At what distance should the object from the lens be placed so that it forms an image at 10 cm from the lens? Also, find the magnification produced by the lens.",tex_environment="minipage} {13 cm}",font_size=35, color=BLUE_C).to_corner(UP,buff=0.2).to_corner(LEFT,buff=0.2)
        ex_title[0].set_color(GREEN)
        for item in ex_title:
            self.play(Write(item))
            self.next_slide()

        sol_label =Tex('Solution :',font_size=35, color=ORANGE).next_to(ex_title,DOWN).align_to(ex_title,LEFT)
        self.play(Write(sol_label)) 

class Ex19(Slide):
    def construct(self):
        ex_title = Tex(r"Example 19 :", r" A 2.0 cm tall object is placed perpendicular to the principal axis of a convex lens of focal length 10 cm. The distance of the object from the lens is 15 cm. Find the nature, position and size of the image. Also find its magnification.",tex_environment="minipage} {13 cm}",font_size=35, color=BLUE_C).to_corner(UP,buff=0.2).to_corner(LEFT,buff=0.2)
        ex_title[0].set_color(GREEN)
        for item in ex_title:
            self.play(Write(item))
            self.next_slide()

        sol_label =Tex('Solution :',font_size=35, color=ORANGE).next_to(ex_title,DOWN).align_to(ex_title,LEFT)
        self.play(Write(sol_label)) 
