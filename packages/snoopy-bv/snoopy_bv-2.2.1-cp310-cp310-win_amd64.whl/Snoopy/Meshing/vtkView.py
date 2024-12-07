"""Contains high-level routines to help the use of VTK
"""

import numpy as np
from Snoopy import logger
from Snoopy.PyplotTools import vtkLookupTable_from_cmap


class CameraManager():
    def __init__(self,  position = [1.,1.,1.],
                        focal_point = [0.,0.,0.],
                        view_angle = 30.0,
                        scale = None,
                        fit_view = 1.0,
                        view_up=[0, 0, 1],
                        bounding_box=None
                ):
        """Handle camera.
        
        Parameters
        ----------
        position : tuple, optional
            Camera position coordinates (x,y,z). The default is [1.,1.,1.].
        focal_point : tuple, optional
            Camera focus point coordinates (x,y,z). The default is [0.,0.,0.].
        view_angle : float, optional
            Angle for perspective view, if False, parallel mode is used. The default is 30.
        scale : float, optional
            scale to use in Parallel mode (viewAngle evaluated to False). The default is None. 
        fit_view : bool or float, optional
            If True, the view is automatically fitted to geometry, a zoom is then applied if fitView is a scalar. The default is 1.0.
        view_up : tuple, optional
            Camera upward position. The default is [0,0,1].
        """

        self.position = position
        self.focal_point = focal_point
        self.view_angle = view_angle
        self.view_up = view_up
        self.scale = scale
        self.fit_view = fit_view
        self.bounding_box = bounding_box

    def set( self, renderer, aspect = None ):
        camera = renderer.GetActiveCamera()

        if self.position is not None:
            camera.SetPosition(self.position)

        if self.focal_point is not None:
            camera.SetFocalPoint(self.focal_point)

        camera.SetViewUp(self.view_up)

        # Persepective mode
        if self.view_angle : 
            camera.SetViewAngle(self.view_angle)
            camera.SetParallelProjection(False)
        else:
            camera.SetParallelProjection(True)

        if self.fit_view :
            self.fit( renderer, aspect = aspect )

        renderer.ResetCameraClippingRange()

        return camera


    def zoom(self, camera, zoom_ratio):
        """Zoom the camera, Use either Dolly or SetParallelScale depending on the perspective mode. 
        """
        # renderer.ResetCameraScreenSpace( offsetRatio )   # Similar to ResetCamera, with addition step ?? In parallel mode, this change the scale. In perspective, it changes the view angle. 
        if self.view_angle :
            camera.Dolly(zoom_ratio)  # .Zoom() would change the view angle, we prefer to change the distance to the focal point.
        else:
            camera.SetParallelScale( camera.GetParallelScale() / zoom_ratio )

        sync_parallel_distance(camera)


    def fit(self, renderer, aspect = None):

        camera = renderer.GetActiveCamera()

        if not self.bounding_box :
            bounding_box = renderer.ComputeVisiblePropBounds()
            logger.debug(f"Bounding box {bounding_box:}")
        else: 
            bounding_box = self.bounding_box

        # Reset the camera,
        #  --> focal point is in the middle of the bounding box.
        #  --> Camera position set so that all actors are in the view.
        renderer.ResetCamera(bounding_box)

        # Zoom after fitting
        if isinstance( self.fit_view, (int, float) ):
            self.zoom( camera, self.fit_view)

        return camera

defaultCamera = CameraManager()


def set_distance_p(vtkCamera, distance):
    """Set distance between focal point and camera position by moving the camera. 
    .SetDistance from VTK method move the focal point.
    """
    focal_point = np.array( vtkCamera.GetFocalPoint() )
    vn = np.array( vtkCamera.GetViewPlaneNormal() )
    vtkCamera.SetPosition( focal_point + distance * vn  )


def sync_parallel_distance(vtkCamera):
    # To update camera "unused" parameter. This allow to keep the same "zoom" when transitioning from perspective to parallel (and vice-versa).
    if vtkCamera.GetParallelProjection():
        distance = vtkCamera.GetParallelScale() /  np.tan(0.5 * ( vtkCamera.GetViewAngle() * np.pi / 180) )
        set_distance_p( vtkCamera, distance )  # vtkCamera.SetDistance( distance ) Set distance move focal point, we prefer to move position here.
    else: 
        scale = vtkCamera.GetDistance() * np.tan(0.5 * (vtkCamera.GetViewAngle() * np.pi / 180))
        vtkCamera.SetParallelScale(scale)


class Camera2D(CameraManager):
    """Base class for the 2D cameras
    """
    def __init__( self, axis = 0, direction = 1, iview_up = 2, vx_lim=None, vy_lim=None, optimize_2d=True, view_angle = False, **kwargs ):
        """To subclass with less argument for the 6 point of view.
 
        Parameters
        ----------
        axis : int, optional
            view axis (0=x, 1=y, 2=z). The default is 0.
        direction : int, optional
            Direction +1 or -1 (To get view from positive or negative direction)
        iview_up : int, optional
            Axis that will point upward. 
        optimize_2d : bool
            If True, the fiew fitting is optimize for 2D (better fill the screen), but not ideal is case of further interactive rotation.
        """
        self.axis = axis
        self.direction = direction
        position = [ 0., 0., 0. ]
        position[axis] = direction
        view_up = [0.0, 0.0 , 0.0]
        view_up[iview_up] = 1.0
        self.iview_up = iview_up

        CameraManager.__init__(self, 
                               position,
                               focal_point = [ 0., 0., 0.],
                               view_angle = view_angle,
                               view_up = view_up,
                               **kwargs,
                               )
        
        # Bounds in the 2D x coordinates system (might correspond, to x, y, on z depending of axis and iview_up)
        # If None, the scaling is adapted to see all actors.
        self.vx_lim = vx_lim  
        self.vy_lim = vy_lim
        self.optimize_2d = optimize_2d

    def fit(self, renderer, aspect = None):

        # Standard VTK view fitting    
        if not self.optimize_2d:
            CameraManager.fit(self, renderer, aspect)
            return
        
        # View fit optimized for 2D "static" case, to better fill the screen, accounts for aspect ratio
        camera = renderer.GetActiveCamera()
        x_min, x_max , y_min, y_max , z_min, z_max = renderer.ComputeVisiblePropBounds()

        bounds = np.array( [ ( x_min, x_max) , ( y_min, y_max) , ( z_min, z_max) ] )

        t = [0,1,2]
        t.remove(self.iview_up)
        t.remove(self.axis)
        ix = t[0]   # Dimension index of the image 'x' coordinates

        if self.vx_lim:
            bounds[ix] = self.vx_lim

        if self.vy_lim:
            bounds[self.iview_up] = self.vy_lim

        center = bounds.mean(axis = 1)

        # Fit ignoring the third dimension.
        bbox = np.array( bounds )
        bbox[self.axis] = 0.0
        logger.debug(f"bbox : {bbox:}")
        renderer.ResetCamera( bbox.flatten() )

        # Centered position and far enough in the view direction (not to be "inside" the mesh)
        center[ self.axis ] = bounds[self.axis][self.direction] + self.direction * 1.0 *(bounds[self.axis][1]-bounds[self.axis][0])
        camera.SetPosition( center )

        # Handle aspect ratio, to be improved, not sure it always works.
        if aspect:
            xrange = bbox[ix][1] - bbox[ix][0]
            yrange = bbox[self.iview_up][1] - bbox[self.iview_up][0]
            data_aspect = xrange / yrange
            logger.debug(f"Data aspect : {data_aspect}")
            logger.debug(f"aspect : {aspect}")
            if data_aspect > 1:
                camera.SetParallelScale( camera.GetParallelScale() / min( aspect, data_aspect ) )

        if isinstance( self.fit_view, (int, float) ):
            self.zoom( camera, self.fit_view)

        return camera


class CameraXP(Camera2D):
    def __init__( self, ylim=None, zlim=None,  **kwargs):
        Camera2D.__init__(self, vx_lim=ylim, vy_lim=zlim, axis = 0, direction = 1, iview_up = 2, **kwargs )

class CameraXM(Camera2D):
    def __init__( self, ylim=None, zlim=None, **kwargs):
        Camera2D.__init__(self, vx_lim=ylim, vy_lim=zlim, axis = 0, direction = -1, iview_up = 2,**kwargs )

class CameraYM(Camera2D):
    def __init__( self, xlim=None, zlim=None, **kwargs):
        Camera2D.__init__(self, vx_lim=xlim, vy_lim=zlim, axis = 1, direction = -1, iview_up = 2,**kwargs )

class CameraYP(Camera2D):
    def __init__( self, xlim=None, zlim=None, **kwargs):
        Camera2D.__init__(self, vx_lim=xlim, vy_lim=zlim, axis = 1, direction = 1, iview_up = 2,**kwargs )

class CameraZP(Camera2D):
    def __init__( self, xlim=None, ylim=None, **kwargs):
        Camera2D.__init__(self, vx_lim=xlim, vy_lim=ylim, axis = 2, direction = 1, iview_up = 1, **kwargs )        

class CameraZM(Camera2D):
    def __init__( self, xlim=None, ylim=None, **kwargs):
        Camera2D.__init__(self, vx_lim=xlim, vy_lim=ylim, axis = 2, direction = -1,iview_up = 1, **kwargs )



class VtkLite():
    """High level layer for handling visualization of single, surface mesh
    """
    def __init__( self, mapper, display_props = {}, camera = defaultCamera, size = (800,600), cbar = False):
        """Class handling simple VTK visualisation.

        Parameters
        ----------
        mapper : vtkMapper
            A vtk mapper
        display_props : dict, optional
            Display properties. The default is {}.
        camera_preset : str, optional
            Camera preset. The default is "default".
        camera_kwds : dict, optional
            Change to preset camera setting. The default is {}.
        cbar : bool, optional
            Whether to display a color bar. The default is False.
            
            
        Parameters display_props
        ------------------------
        cell_field : str
            Field used to color the mesh
        point_field : str
            Field used to color the mesh
        color : tuple
            RGB color
            
        Parameters camera_kwds
        ------------------------
        fitView : float or None
            Automatic zoom.
              
            
        Example
        -------
        >>> v = msh.vtkView.VtkLite.FromMesh(m, camera = ,  display_props = {"edges" : 1 , "color" : [1.0, 0.0, 0.0]})
        >>> v.to_interactive( size = (800,300) )
        
        """
        import vtk
        self.mapper = mapper
        self.actor = vtk.vtkActor()
        self.actor.SetMapper(mapper)

        self.renderer = vtk.vtkRenderer()
        # self.renderer.SetAspect(aspect)
        self.renderer.AddActor(self.actor)
        self.renderer.SetBackground(1, 1, 1)  # White background
        
        # Should be put in "view" routines?
        self.set_properties(display_props)

        self.camera = camera

        self.size = size
        
        self.camera.set(self.renderer, aspect = size[0] / size[1])
        
        if cbar:
            self.renderer.AddActor(addColorBar(self.actor, title= display_props.get("cell_field" , display_props.get("point_field", "" )) ))
        

    def set_properties(self, display_props):
        setDisplayProperties(self.actor, **display_props)

            
        
    @classmethod
    def FromPolydata(cls, polydata, **kwargs):
        import vtk
        mapper = vtk.vtkDataSetMapper()
        mapper.SetInputData( polydata )
        return cls(mapper , **kwargs)
    
    
    @classmethod
    def FromVtuFile(cls, vtk_file, *args, **kwargs):
        import vtk
        r = vtk.vtkUnstructuredGridReader()
        r.SetFileName(vtk_file)
        r.Update()
        mapper = vtk.vtkDataSetMapper()
        mapper.SetInputConnection(r.GetOutputPort())
        return cls( mapper , *args, **kwargs )
    
    @classmethod
    def FromMesh(cls, mesh, *args, **kwargs):
        p = mesh.convertToVtk()
        return cls.FromPolydata(p, *args, **kwargs)


    def set_osp_ray(self):
        print("Using ospray")
        import vtk
        osprayPass = vtk.vtkOSPRayPass()

        self.renderer.SetPass(osprayPass)

        osprayNode = vtk.vtkOSPRayRendererNode()
        osprayNode.SetEnableDenoiser(1, self.renderer)

        osprayNode.SetSamplesPerPixel(4,self.renderer)
        osprayNode.SetAmbientSamples(0,self.renderer)
        osprayNode.SetMaxFrames(4, self.renderer)

        osprayNode.SetRendererType("pathtracer", self.renderer);

        osprayNode.SetBackgroundMode(osprayNode.Environment, self.renderer)

        self.renderer.SetEnvironmentUp( -1 , 0. , 0.0)
        self.renderer.SetEnvironmentRight( 0 , -1 , 0)

        self.renderer.SetEnvironmentalBG(0.0, 0.9, 0.0)
        self.renderer.SetEnvironmentalBG2(0.0, 0.9, 0.0)
        self.renderer.GradientEnvironmentalBGOn()

        ml = vtk.vtkOSPRayMaterialLibrary()
        ml.AddMaterial("metal_1", "thinGlass")
        ml.AddShaderVariable("metal_1", "attenuationColor", 3,  [ 0.0, 0.9, 0.0 ])

        osprayNode.SetMaterialLibrary(ml, self.renderer)
        self.actor.GetProperty().SetMaterialName("metal_1")
        self.actor.GetProperty().SetEdgeVisibility(1)


    def add_line(self, start , stop, display_props = {} ):
        """Add a line to the view.

        Parameters
        ----------
        start : tuple
            XYZ coordinates
        stop : TYPE
            XYZ coordinates
        display_props : dict, optional
            Argument passed to setDisplayProperties. The default is {}.
        """
        import vtk
        
        ls = vtk.vtkLineSource()
        ls.SetPoint1(*start)
        ls.SetPoint2(*stop)

        m = vtk.vtkDataSetMapper()
        m.SetInputConnection( ls.GetOutputPort() )

        a = vtk.vtkActor()
        a.SetMapper(m)

        setDisplayProperties( a,  **display_props )
        self.renderer.AddActor(a)


    def to_picture(self, output_file ) :
        """Write image file

        Parameters
        ----------
        output_file : str
            Filename
        size : tuple, optional
            Picture resolution, default to None (use the one from the object).
        """
        renderer_to_picture( self.renderer, output_file , size = self.size )


    def to_numpy(self) : 
        """Return image array (RGB table).

        Parameters
        ----------
        size : tuple
            Resolution

        Returns
        -------
        np.ndarray
            The pixel array
        """
        return renderer_to_numpy( self.renderer, size = self.size )
        
        
    def to_interactive(self ):
        """Open interactive visualizer.

        Parameters
        ----------
        size : tuple, optional
            Resolution, by default (800,600)
        """
        import vtk
        renderWindow = vtk.vtkRenderWindow()
        renderWindow.AddRenderer( self.renderer )
        renderWindowInteractor = vtk.vtkRenderWindowInteractor()
        renderWindowInteractor.SetRenderWindow(renderWindow)
        renderWindowInteractor.SetInteractorStyle( vtk.vtkInteractorStyleTrackballCamera() )
        
        renderWindow.SetSize( self.size )
        
        renderWindow.Render()
        renderWindowInteractor.Start()

    def to_notebook(self,  **kwargs):
        """Display in notebook"""

        return vtk_show( self.renderer, size = self.size, **kwargs )



def writerFromExt(ext):
    """Pick correct vtk writter class based on extension

    Parameters
    ----------
    ext : srt
        File extension of filename, among [.png, .jpg, .bmp, .eps, .tiff]

    Returns
    -------
    writer : vtk.vtkWriter
        Writer class
    """
    import vtk

    ext_ = ext.split(".")[-1]

    if ext_ == "png":
        writer = vtk.vtkPNGWriter
    elif ext_ == "jpg":
        writer = vtk.vtkJPEGWriter
    elif ext_ == "bmp":
        writer = vtk.vtkBMPWriter
    elif ext_ == "eps":
        writer = vtk.vtkPostScriptWriter
    elif ext_ == "tiff":
        writer = vtk.vtkTIFFWriter
    else:
        raise (Exception(f"Picture extension not recognized : {ext:}"))
    return writer



def get_camera_kwds(cam):
    return {
            "camPosition"    : cam.GetPosition(),
            "targetPosition" : cam.GetFocalPoint(),
            "viewAngle"   : None if cam.GetParallelProjection() else cam.GetViewAngle() ,
            "fitView" : False,
            "scale"   : cam.GetParallelScale() ,
           }


def printCamera(cam):
    return f"{get_camera_kwds(cam):}"


def setCamera(
    renderer,
    camPosition=None,
    targetPosition=None,
    viewAngle=30.0,
    scale=None,
    fitView = 0.9,
    viewUp=[0, 0, 1],
    boundingBox=None,
    ):
    """Set camera positon

    For compatibility purpose. CameraManager is now recommanded.

    Parameters
    ----------
    renderer : vtk.vtkRenderer
        The vtk renderer
    camPosition : tuple, optional
        Camera position coordinates (x,y,z). The default is None.
    targetPosition : tuple, optional
        Camera focus point coordinates (x,y,z). The default is None.
    viewAngle : float, optional
        Angle for perspective view, if False, parallel mode is used. The default is 30.
    scale : float, optional
        scale to use in Parallel mode (viewAngle evaluated to False). The default is None. 
    fitView : bool or float, optional
        If True, the view is automatically fitted to geometry, a zoom is then applied if fitView is a scalar. The default is True.
    viewUp : tuple, optional
        Camera upward position. The default is [0,0,1].
    """
    cm = CameraManager( position = camPosition,
                        focal_point = targetPosition,
                        view_angle = viewAngle,
                        scale = scale,
                        fit_view = fitView,
                        view_up=viewUp, 
                        bounding_box = boundingBox )
    
    return cm.set(renderer)

    


def setDisplayProperties(
    actor,
    cell_field = None,
    point_field = None,
    cmap="cividis",
    scalarRange = None,
    edges=0,
    opacity=1.0,
    component = None,
    color = [0.5,0.5,0.5],
    linewidth = 1.0,
    update_mapper = False,
    point_size = 5.0
):
    """Specify field to use to mapper

    Parameters
    ----------
    mapper : vtk.vtkMapper
        The mapper
    scalarField : str
        field to plot
    scalarRange : tuple, None or "auto"
        Color map bounds. if "auto", datarange is used (might not work if several time steps)
    cmap : str or vtk.vtkLookUpTable
        Color map
    update_mapper : bool
        Whether to update the mapper before applying the properties, this is only useful for actual check of field availability.
    """

    mapper = actor.GetMapper()
    
    if scalarRange == "auto" :
        update_mapper = True

    if update_mapper:     
        mapper.Update()

    if cell_field or point_field:
        
        if cell_field : 
            data_source = "cell"
            cd = mapper.GetInputAsDataSet().GetCellData()
            available_field = [ cd.GetArrayName(i) for i in range(cd.GetNumberOfArrays()) ]
            if cell_field not in available_field and not update_mapper :
                logger.debug( f"{cell_field:} not available in {available_field:}" )

            mapper.SetScalarModeToUseCellFieldData()
            mapper.SelectColorArray(cell_field)
        else: 
            data_source="point"
            cd = mapper.GetInputAsDataSet().GetPointData()
            available_field = [ cd.GetArrayName(i) for i in range(cd.GetNumberOfArrays()) ]
            if point_field not in available_field and not update_mapper :
                logger.debug( f"{point_field:} not available in {available_field:}" )
            
            mapper.SetScalarModeToUsePointFieldData()
            mapper.SelectColorArray(point_field)
            
        # mapper.SetUseLookupTableScalarRange(0)
        if scalarRange is not None:
            if scalarRange == "auto":
                # FIXME : there is probably a simpler and more general way...
                try:
                    if data_source.lower() == "cell":
                        sr = (
                            mapper.GetInputAsDataSet()
                            .GetCellData()
                            .GetArray(cell_field)
                            .GetValueRange()
                        )
                    if data_source.lower() == "point":
                        sr = (
                            mapper.GetInputAsDataSet()
                            .GetPointData()
                            .GetArray(point_field)
                            .GetValueRange()
                        )
                        
                except Exception:
                    logger.warning(
                        f"{cell_field:} {point_field} not there yet. Cannot set color map range"
                    )
            else:
                sr = scalarRange


            mapper.SetScalarRange(*sr)
            mapper.SetUseLookupTableScalarRange(False)
         
        
        if isinstance(cmap, str):
            lut = vtkLookupTable_from_cmap(cmap)
        else:
            lut = cmap

        mapper.SetLookupTable(lut)

        if component is not None:
            mapper.GetLookupTable().SetVectorComponent(component)
            lut.SetVectorModeToComponent()
        else : 
            lut.SetVectorModeToMagnitude()
    else :
        mapper.SetScalarVisibility(False)
        actor.GetProperty().SetColor( color )
        
    # Properties
    prop = actor.GetProperty()
    prop.SetEdgeVisibility(edges)
    prop.SetOpacity(opacity)
    prop.SetLineWidth( linewidth )
    prop.SetPointSize( point_size )
    prop.SetRenderPointsAsSpheres(True)


def addColorBar(actor, title="?", width=0.05, height=0.25):
    """Create color bar actor

    Parameters
    ----------
    actor : vtk.vtkActor
        The actor

    Return
    ------
    vtk.vtkScalarBarActor
       The color bar actor
    """
    import vtk

    # --- Color bar legend
    lut = actor.GetMapper().GetLookupTable()
    scalarBar = vtk.vtkScalarBarActor()
    scalarBar.SetLookupTable(lut)
    scalarBar.SetWidth(width)
    scalarBar.SetHeight(height)
    scalarBar.SetTitle(title)
    scalarBar.GetTitleTextProperty().SetColor(0.0, 0.0, 0.0)
    scalarBar.GetLabelTextProperty().SetColor(0.0, 0.0, 0.0)
    return scalarBar


def renderer_to_picture(renderer, pictureFile, size = (1650, 1050), mag = 1,  large_image = False ):
    """Set camera positon

    Parameters
    ----------
    renderer : vtk.vtkRenderer
        The vtk renderer
    pictureFile : str
        Output picture name
    size : tuple(float)
        Resolution of the output picture, if none, the current/default renderering size is used.
    mag : int
        Magnification factors
    large_image : bool
        If True, uses vtkRenderLargeImage, which does not need a new rendering window (instead of vtkWindowToImageFilter).
    """

    w2if = _renderer_to_vtk_image( renderer, size = size, mag = mag,  large_image = large_image  )
    w = writerFromExt(pictureFile[-4:])()
    w.SetFileName(pictureFile)
    w.SetInputConnection(w2if.GetOutputPort())
    w.Write()
    logger.debug(f"{pictureFile:} written")
    

def renderer_to_numpy(renderer, size = (1650, 1050), mag = 1,  large_image = False ):
    from vtk.util.vtkImageExportToArray import vtkImageExportToArray
    w2if = _renderer_to_vtk_image( renderer, size = size, mag = mag,  large_image = large_image  )
    w2if.Update()
    c = vtkImageExportToArray()
    c.SetInputConnection( w2if.GetOutputPort() )
    return c.GetArray()[0,::-1,::,::]
    
    

def _renderer_to_vtk_image( renderer, size = (1650, 1050), mag = 1,  large_image = False  ):
    import vtk
    if large_image:
        w2if = vtk.vtkRenderLargeImage()
        w2if.SetMagnification(mag)  # => multiply the resolution of the picture
        w2if.SetInput(renderer)
        w2if.Update()
    else:
        renWin = vtk.vtkRenderWindow() # --- Rendering windows
        renWin.SetOffScreenRendering(1)
        renWin.AddRenderer(renderer)
        if size is None: 
            size = renWin.GetSize()
        renWin.SetSize( mag*size[0], mag * size[1] )
        w2if = vtk.vtkWindowToImageFilter()
        w2if.SetInput(renWin)
        w2if.Update() # .Modified
    return w2if


def vtk_show(renderer, size = None):
    """Takes vtkRenderer instance and returns an IPython Image with the rendering.

    To be used in jupyter notebook to vizualize a vtk image.
    """
    import vtk
    from IPython.display import Image
    renderWindow = vtk.vtkRenderWindow()
    renderWindow.SetOffScreenRendering(1)
    renderWindow.AddRenderer(renderer)

    if size :
        renderWindow.SetSize( *size )

    renderWindow.Render()

    windowToImageFilter = vtk.vtkWindowToImageFilter()
    windowToImageFilter.SetInput(renderWindow)
    windowToImageFilter.Update()

    writer = vtk.vtkPNGWriter()
    writer.SetWriteToMemory(1)
    writer.SetInputConnection(windowToImageFilter.GetOutputPort())
    writer.Write()
    data = memoryview(writer.GetResult()).tobytes()

    return Image(data)



#For backward compatibility
def viewPolyData( polydata, *args,**kwargs):
    VtkLite.FromPolydata( polydata, *args,**kwargs ).to_interactive()


def pictureFromSingleVtk( vtkFile, picture_file, **kwargs ):
    """Set camera positon

    Parameters
    ----------
    vtkFile : str
        The vtk file
    pictureFile : str
        Output picture name
    camSettings : dict, optional
        Camera settings
    """
    
    VtkLite.FromVtuFile( vtkFile, **kwargs ).to_picture(picture_file)
    
