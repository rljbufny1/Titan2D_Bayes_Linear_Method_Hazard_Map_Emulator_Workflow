sim=TitanSimulation(overwrite_output=True)

sim.setGIS(
   gis_format='GIS_GRASS',
   gis_main='../grassdata',
   gis_sub='location',
   gis_mapset='PERMANENT',
   gis_map='map',
   gis_vector=None,
   region_limits=None
)

sim.setScale(
   length_scale=10000.0,
   gravity_scale=9.8,
   height_scale=None
)

sim.setNumProp(
   AMR=True,
   number_of_cells_across_axis=64,
   order='First'
)

sim.setMatModel(
   model='Coulomb',
   use_gis_matmap=False,
   stopping_criteria=None,
   int_frict=30.0,
   bed_frict=24.0
)

sim.setTimeProps(
   max_iter=300,
   max_time=100.0
)

sim.setRestartOutput(
    dtime=None,
    diter=None,
    keep_all=False,
    keep_redundant_data=False,
    output_prefix='restart'
)

sim.setStatProps(
   runid=-1,
   edge_height=None,
   test_height=None,
   test_location=None,
   output_prefix=''
)

sim.setOutlineProps(
   enabled=True,
   max_linear_size=1024.0,
   init_size='AMR',
   output_prefix=''
)

sim.addPile(
   pile_type='Paraboloid',
   height=50.0,
   center=[645000.0, 2165000.0],
   radii=[10000.0, 5000.0],
   orientation=-45.0,
   Vmagnitude=2.0,
   Vdirection=-5.0
)

sim=sim.run()

