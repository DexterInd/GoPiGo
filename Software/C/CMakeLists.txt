cmake_minimum_required(VERSION 3.0)
project(gopigo VERSION 1.6)

if(CMAKE_INSTALL_PREFIX_INITIALIZED_TO_DEFAULT)
    set(CMAKE_INSTALL_PREFIX "/usr" CACHE PATH "Install path prefix prepended on to install directories." FORCE)
endif(CMAKE_INSTALL_PREFIX_INITIALIZED_TO_DEFAULT)

# define static and shared libraries
add_library(gopigo_shared SHARED gopigo.c)
add_library(gopigo_static STATIC gopigo.c)
# save both libraries under same name with different extensions
# => libgopigo.{a,so}
set_target_properties(gopigo_shared gopigo_static PROPERTIES OUTPUT_NAME gopigo)
set_target_properties(gopigo_shared gopigo_static PROPERTIES VERSION ${PROJECT_VERSION})

# executable to test library function
add_executable(basic_test_all basic_test_all.c)
target_link_libraries(basic_test_all gopigo_shared)

# library configuration files
set(PACKAGE_NAME gopigo)
set(GOPIGO_VERSION ${PROJECT_VERSION})
set(prefix      ${CMAKE_INSTALL_PREFIX})
set(exec_prefix ${CMAKE_INSTALL_PREFIX})
set(libdir      ${CMAKE_INSTALL_PREFIX}/lib)
set(includedir  ${CMAKE_INSTALL_PREFIX}/include)
set(LIBS        "-lgopigo")
configure_file(gopigo.pc.in ${CMAKE_CURRENT_BINARY_DIR}/gopigo.pc)
configure_file(cmake/gopigoConfig.cmake.in ${CMAKE_CURRENT_BINARY_DIR}/gopigoConfig.cmake)
configure_file(cmake/gopigoConfigVersion.cmake.in ${CMAKE_CURRENT_BINARY_DIR}/gopigoConfigVersion.cmake)

# installation
install(TARGETS gopigo_shared DESTINATION lib COMPONENT dev)
install(TARGETS gopigo_static DESTINATION lib COMPONENT dev)
install(FILES gopigo.h DESTINATION include COMPONENT dev)
install(FILES ${CMAKE_CURRENT_BINARY_DIR}/gopigo.pc DESTINATION lib/pkgconfig COMPONENT dev)
install(FILES
  ${CMAKE_CURRENT_BINARY_DIR}/gopigoConfig.cmake
  ${CMAKE_CURRENT_BINARY_DIR}/gopigoConfigVersion.cmake
  DESTINATION lib/cmake/${PACKAGE_NAME} COMPONENT dev)
install(TARGETS basic_test_all DESTINATION bin COMPONENT executable)

# package generation
set(CPACK_GENERATOR "DEB")
# install to CMAKE_INSTALL_PREFIX instead of default /usr/
set(CPACK_SET_DESTDIR ON)
set(CPACK_DEBIAN_PACKAGE_MAINTAINER "Dexter Industries")
set(CPACK_PACKAGE_NAME libgopigo)
set(CPACK_PACKAGE_VERSION ${PROJECT_VERSION})
set(CPACK_PACKAGE_DESCRIPTION_SUMMARY "library to access GoPiGo driven robots")
set(CPACK_PACKAGE_VENDOR "Dexter Industries")

set(CPACK_STRIP_FILES ON)
set(CPACK_COMPONENTS_ALL dev)
set(CPACK_DEB_COMPONENT_INSTALL ON)
include(CPack)

