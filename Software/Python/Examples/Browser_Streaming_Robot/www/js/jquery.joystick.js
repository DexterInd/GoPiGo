// This code is a modified version of https://github.com/mifi/jquery-joystick

// http://stackoverflow.com/questions/2162981/jquery-plugin-authoring-set-different-options-for-different-elements
// http://learn.jquery.com/plugins/advanced-plugin-concepts/
(function($) {
    $.fn.joystick = function(val, arg1, arg2) {
        var getValue = function() {
            var $joystick = $(this);
            var $innerCircle = $(this).children('.inner_circle');
            var $handle = $(this).children('.handle');

            var innerCircleRadius = $innerCircle.width()/2;
            var innerCircleCentreX = $innerCircle.position().left + innerCircleRadius;
            var innerCircleCentreY = $innerCircle.position().top + innerCircleRadius;
            
            var handleCentreX = $handle.position().left + $handle.width()/2;
            var handleCentreY = $handle.position().top + $handle.height()/2;
            
            var x = (handleCentreX - innerCircleCentreX)/innerCircleRadius;
            var y = -(handleCentreY - innerCircleCentreY)/innerCircleRadius;
            return {x: x, y: y};
        };

        var setValue = function(x, y) {
            var $joystick = $(this);
            var $innerCircle = $(this).children('.inner_circle');
            var $handle = $(this).children('.handle');

            var innerCircleRadius = $innerCircle.width()/2;
            var innerCircleCentreX = $innerCircle.position().left + innerCircleRadius;
            var innerCircleCentreY = $innerCircle.position().top + innerCircleRadius;
            
            var left = innerCircleCentreX + x*innerCircleRadius - $handle.width()/2;
            var top = innerCircleCentreY - y*innerCircleRadius - $handle.height()/2;
            $handle.css('left', left);
            $handle.css('top', top);

            $joystick.data('joystick-options').moveEvent.call(
                $joystick, getValue.call(this) );
        };
        
        

        // Init
        if (typeof val === 'object') {
            var options = $.extend({
                xAxis: true,
                yAxis: true,
                xSnap: false,
                ySnap: false,
                moveEvent: function() {},
                endEvent: function() {},
                clickEvent: function() {},
                updateIntervalMS: 0,
                updateEvent: function() {},
            }, val);

            this.data('joystick-options', options);

            return this.each(function() {
                var $joystick = $(this);
                var $innerCircle = $(this).children('.inner_circle');
                var $handle = $(this).children('.handle');

                var innerCircleRadius = $innerCircle.width()/2;
                var innerCircleLeft = $joystick.width()/2 - $innerCircle.width()/2;
                var innerCircleTop = $joystick.height()/2 - $innerCircle.height()/2;
                var innerCircleCentreX = innerCircleLeft + innerCircleRadius;
                var innerCircleCentreY = innerCircleTop + innerCircleRadius;
                
                $innerCircle.css('left', innerCircleLeft );
                $innerCircle.css('top', innerCircleTop );
                
                $handle.css('left', innerCircleCentreX - $handle.width()/2);
                $handle.css('top', innerCircleCentreY - $handle.height()/2);

                if ($joystick.data('joystick-options').updateIntervalMS > 0) {
                    setInterval( function() {
                        $joystick.data('joystick-options').updateEvent.call($joystick[0], getValue.call($joystick));
                    }, $joystick.data('joystick-options').updateIntervalMS );
                }
                
                $joystick.on('touchstart mousedown', function(e) {
                    e.preventDefault();
                    $joystick.data('clicked', true);
                    $joystick.data('clickStartTime', new Date().getTime() );
                });

                // TODO Touchcancel
                $joystick.on('touchend mouseup mouseleave', function(e) {
                    e.preventDefault();
                    $joystick.data('clicked', false);
                    
                    var clickEndPos = getValue.call($joystick[0]);
                    var clickEndTime = new Date().getTime();
                    if ( clickEndTime - $joystick.data('clickStartTime') <= 1000 )
                    {
                        $joystick.data('joystick-options').clickEvent.call( $joystick[0], clickEndPos );
                    }
                    
                    
                    if ($joystick.data('joystick-options').xSnap) {
                        setValue.call($joystick[0], 0.0, getValue.call($joystick[0]).y);
                    }
                    if ($joystick.data('joystick-options').ySnap) {
                        setValue.call($joystick[0], getValue.call($joystick[0]).x, 0.0);
                    }

                    $joystick.data('joystick-options').endEvent.call($joystick[0], getValue.call(this));
                });

                $joystick.on('touchmove mousemove', function(e) {
                    e.preventDefault();
                        
                        var pageX;
                        var pageY;
                        if ( e.type == 'mousemove' )
                        {
                            pageX = e.pageX;
                            pageY = e.pageY;
                        }
                        else
                        {
                            var touch = e.originalEvent.targetTouches[0];
                            pageX = touch.pageX;
                            pageY = touch.pageY;
                        }
                        
                    var x = pageX - ($joystick.offset().left + innerCircleCentreX);
                    var y = pageY - ($joystick.offset().top + innerCircleCentreY);

                    if ($joystick.data('clicked')) {
                        
                        var distanceFromCentre = Math.sqrt( x*x + y*y );
                        if ( distanceFromCentre > innerCircleRadius )
                        {
                            x = (x / distanceFromCentre)*innerCircleRadius;
                            y = (y / distanceFromCentre)*innerCircleRadius;
                        }
                        
                        var handleLeft = innerCircleCentreX + x - $handle.width()/2;
                        var handleTop = innerCircleCentreY + y - $handle.height()/2;

                        if ($joystick.data('joystick-options').xAxis) {
                            $handle.css('left', handleLeft);
                        }
                        if ($joystick.data('joystick-options').yAxis) {
                            $handle.css('top', handleTop);
                        }

                        $joystick.data('joystick-options').moveEvent.call($joystick[0], getValue.call(this));
                    }
                });
            });
        }
        else if (typeof val === 'string') {
            switch (val.toLowerCase()) {
                case 'value':
                if (arg1 === undefined) {
                    return getValue.call(this[0]);
                }
                else {
                    return this.each(function() {
                        setValue.call(this, arg1, arg2);
                    });
                }
            }
        }
    };
}( jQuery ));
